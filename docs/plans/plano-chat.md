# Plano — Chat mascarado denunciante ↔ helper (decisão 54)

> **Rodada 12 — FECHADA em 2026-09-03** (rodada 0 e rodada 1 no mesmo
> dia). Decisões **168–177** registradas no
> [VGR-plano.md](../decisions/VGR-plano.md). Execução C1 → C2 → C3, cada
> fase liberada por "pode seguir" (38). **C1 executada em 2026-09-03** (api `8af91a8`); C2 aguarda liberação.

---

## 1. Contexto

A decisão 54 colocou o chat no MVP: **texto simples, sem compartilhar
contato direto, com as mesmas restrições de anonimato das categorias de
risco (40)**, como Bounded Context novo. A spec tática desenhou o agregado
`ChatThread` (um por par Report + Helper, `participantMask` com
`MaskedIdentity` = token opaco por (thread, usuário), nunca reusado entre
reports) e dois cenários (`004`, emendados em 2026-08-22: "nenhum código
existe"). Hoje o laço denunciante ↔ helper **termina na oferta de ajuda**:
o helper oferece (tipo de ajuda), o denunciante vê a oferta, e não há
canal nenhum entre os dois.

**O que já existe e condiciona o desenho (evidência, 2026-09-03):**

| Peça | Estado | Consequência para o chat |
|---|---|---|
| `tb_help_offer` (`helper_account_id` NULL quando anônimo sem conta; `anonymous='S'` quando conta escolheu anonimato) | R3 | Helper **sem conta** não tem identidade nenhuma no servidor depois da oferta — não há como rotear mensagem para ele |
| Denunciante anônimo | `x-client-key` (bearer secret, 134/137) prova posse do report | Denunciante sem conta **pode** ser participante do chat pelo mesmo mecanismo |
| Visibilidade de identidade na oferta (`HelpOfferView`, 6/40/41/60) | nome só se o helper escolheu **e** tier ≠ high; timestamps nunca em tier high | A regra de máscara do chat deve ser a MESMA, ou a superfície mais permissiva vaza |
| Anonimato total do helper (55) | outros helpers não veem identidade | Thread é estritamente bilateral; nunca "sala" |
| Degradação temporal por tier (`TIME_MS_BY_TIER`, 41/135) | feed e detalhe | Timestamp de mensagem é sinal temporal — precisa de regra |
| Notificação push | **fora do MVP** (11); nenhuma infra de push, SSE ou websocket na API nem no app | Entrega precisa ser por polling ou abrir infra nova |
| Fila offline (28/123) | denúncia e anexos | Mensagem pode entrar na fila ou não |
| Retenção (25/131), congelamento (141), purge (`purgeReport` zera detail/posição/payloads) | R3 | Mensagens são evidência da mesma natureza: entram na mesma régua |
| Moderação (162/167), fila (161), leitura auditada no painel (166) | frente 142 | Chat é onde abuso e retaliação tendem a acontecer — o painel precisa de leitura, auditada |
| Legal Gate (76–79): capacidade nova nasce `PENDING_WIRING` | vigente | `chat.masked` como capacidade |
| `vgr_validators` (153–157) | espelho de regra API→app | filtro anti-contato pode ter espelho no app |

## 2. Invariantes que a frente NÃO pode tocar

- Máscara é obrigatória e **nunca** menos restritiva que a da oferta
  (6/40/55/60): identidade de quem é anônimo não aparece para ninguém
  fora da plataforma; em tier high ninguém se identifica para ninguém.
- Thread é **bilateral**: um por (report, helper); denunciante vê N
  threads, cada helper vê só a sua (55).
- A plataforma sempre sabe quem é quem (23/60) — `participantMask`
  guarda o vínculo interno; o que sai da API é o token.
- Anti-fraude de papel (20): denunciante não conversa consigo mesmo.
- Retenção/congelamento/purge valem para mensagens (25/131/141).
- Nada de contato direto (54) — a regra é do servidor; o app só antecipa.
- Sem mídia no chat (54: "texto simples"); anexos continuam no report.
- Erro só em inglês com `code` (80/83); enforcement no servidor (72/110).
- Nenhum widget Flutter direto (133); validação via `vgr_validators`.

## 3. Objetivos (confirmados pelas decisões 168–177)

1. Denunciante e helper vinculados por oferta trocam texto dentro do app,
   sem nenhum dos dois saber mais do outro do que a oferta já mostrava.
2. Contato direto não atravessa o canal.
3. Mensagens chegam sem push (MVP), com latência aceitável na tela.
4. Chat segue o ciclo de vida do caso e a régua de retenção.
5. O painel lê o chat de um caso, auditado, sob grant próprio, para
   moderar retaliação e abuso.
6. Capacidade no Legal Gate, testes de máscara e de filtro, docs.

## 4. Fatiamento (decisão 168 — C1 → C2 → C3)

| Fase | Entrega | Depende de |
|---|---|---|
| **C1 — API** — **EXECUTADA em 2026-09-03** (api `8af91a8`) | Módulo `messaging` em `/app-chat` (plano do app, `optionalAppAuth` + `x-client-key`): migração 043 (`tb_chat_thread` único por (report, helper_account), `tb_chat_participant` com token opaco de 32 hex, `tb_chat_message` único por (thread, clientKey), capacidade `chat.masked`); `GET /:reportId/threads`, `POST /:reportId/messages` (helper com conta+oferta, find-or-create), `GET|POST /threads/:threadId/messages` (cursor `after`, ponteiro de leitura privado); filtro anti-contato em `shared/chat/contact-filter.ts` (422 `CONTACT_NOT_ALLOWED` com `kind`/`match`); gate antes de qualquer escrita (451); `CHAT_CLOSED` 409 em resolvido/oculto; congelado segue; purge zera texto na mesma transação do report; `RATE_LIMITED` 429 por thread/participante (env); timestamps degradados por tier; accountability para denunciante anônimo; visões owner/participant do caso ganham `chat`. Specs 003/004 emendadas; `docs/feature/chat.md`. Suíte: 88/832. Migração 043 aplicada em dev. **Anotado**: `face` na lista de mensageiros gera falso positivo ("em face de 3 pessoas") — revisar na C2 com uso real | — |
| **C2 — Mobile** — **EXECUTADA em 2026-09-03** (app `7c75d4f`; API `b13ed6a` tirou `face` da lista de mensageiros) | Módulo `chat` (`/chat/threads/:reportId`, `/chat/:reportId/thread/:threadId|new`): lista de conversas do denunciante, tela de conversa com polling por cursor a cada 5 s só com a tela visível (pausa em background), envio pela fila offline (`chat.post`, `clientKey` UUID, bolha otimista → confirmada ou falhada sem retry em 422/409/451), aviso de thread fechada, papéis renderizados como servidos (denunciante nunca nomeado); `VgrValidators.noDirectContact` espelha o filtro da API fixture por fixture (91 testes no pacote); widgets novos `VgrChatBubble`/`VgrChatComposer`/`VgrChatMessageList`/`VgrBadge`; botão de chat no detalhe pelo facet `chat`; aviso ao helper sem conta no formulário de oferta (169). Suítes: mobile 200, validators 91, widgets 19, admin 273. Doc `app/docs/feature/chat.md`. **Anotado**: `MyReportsStore` importado pelo módulo chat (mesmo precedente do help_offer) — promover a `app/shared/` quando houver 3º consumidor; ciclo de vida em background coberto por teste de bloc, não em aparelho | C1 |
| **C3 — Painel** — **EXECUTADA em 2026-09-03** (api `42f8408`, app `cdcc478`) | Migração 044 (`chat_evidence` R, VIEW, SEM bootstrap — aplicada em dev); `GET /api/reports/:id/chat` montado pelo gateway no router do módulo messaging (sem import cruzado), `reports` VIEW + `chat_evidence` VIEW empilhados, uma linha de auditoria por leitura (`report_chat`), no-store, só leitura; identidade do plano do painel (helper sempre identificável internamente com `anonymousChoice`, denunciante só se o caso não é anônimo); timestamps exatos; texto purgado = null. Admin: seção "Chat (evidência)" no detalhe só com o grant, carregada sob demanda, cards por thread, sem compositor. Suítes: API 90/869, admin 286 | C1 |

## 5. Alternativas que estavam em cima da mesa (escolhas nas decisões 169–177)

### 5.1 Quem pode conversar (pergunta 2)
- (i) **Só quem tem identidade roteável**: helper com conta (mesmo tendo
  escolhido anonimato — a máscara cobre); denunciante com conta **ou** com
  `x-client-key`. Helper sem conta não tem chat, e o app avisa antes da
  oferta (mesmo padrão do aviso "sem conta não reivindica recompensa", 34).
- (ii) Bearer secret também para o helper sem conta (chave gerada na
  oferta, devolvida ao app, guardada localmente): cobre 100% dos helpers,
  mas cria um segundo segredo portador e a fila de "quem é esse helper"
  depende do aparelho.
- (iii) Chat só entre contas (denunciante anônimo sem conta fica sem chat).

### 5.2 O que cada lado vê do outro (pergunta 3)
- (i) **Mesma regra da oferta**: rótulo fixo "Denunciante" / "Ajudante";
  nome de exibição só quando o helper escolheu identificar-se **e** tier ≠
  high; denunciante nunca mostra nome (ele não tem escolha equivalente
  hoje). Token opaco por (thread, participante) no payload (spec).
- (ii) Nome de exibição de ambos quando ambos identificados e tier ≠ high.
- (iii) Rótulo fixo sempre, nunca nome.

### 5.3 Anti-contato (pergunta 4)
- (i) **Bloqueio no servidor** por padrão (telefone com ≥ 8 dígitos,
  e-mail, URL, `@handle`, "whats/zap/telegram/insta" + número) → 422
  `CONTACT_NOT_ALLOWED` com o trecho ofendido; regra em `shared/` e
  **espelho no app** via `vgr_validators` (154) para feedback antes do
  envio. Texto máx. 1000 chars.
- (ii) Só aviso no app, servidor aceita.
- (iii) Mascarar no servidor (substituir por `[removido]`) e entregar.

### 5.4 Entrega e fila offline (pergunta 5)
- (i) **Polling com cursor** (`after=<messageId>`), intervalo curto só com
  a tela aberta (ex. 5 s), sem background; contagem de não lidas no
  detalhe do caso quando ele é aberto. Push fica como visão (11).
- (ii) SSE (`text/event-stream`) na API — infra nova, mas simples.
- (iii) Websocket — infra nova de verdade (proxy, escala).
- Fila offline (28): mensagem entra na fila e sobe quando houver rede
  (idempotência por `clientKey` da mensagem, como a denúncia 137)? Ou chat
  exige rede (erro imediato)?

### 5.5 Ciclo de vida (pergunta 6)
- Thread nasce **find-or-create** na primeira mensagem do helper com
  oferta (spec) — ou na própria oferta?
- Caso **resolvido**: leitura mantida até o purge (18/131); escrita —
  fechada (i) ou aberta por N dias (ii)?
- Caso **oculto** (162): escrita fechada, leitura mantida (i)?
- Caso **congelado** (141): tudo mantido, escrita segue (i)?
- **Purge** (131): mensagens apagadas junto (texto zerado, esqueleto de
  contagem mantido para estatística) — (i).

### 5.6 Timestamps e sinais (pergunta 7)
- (i) Timestamp de mensagem **degradado por tier** para o outro lado
  (`TIME_MS_BY_TIER`: minuto/15 min/hora) — coerente com 41; ordem
  preservada pelo id.
- (ii) Exato para os dois participantes (a conversa já é sinal), degradado
  só para o painel/estatística.
- Recibo de leitura ("visto") — (i) não existe no MVP; (ii) existe.

### 5.7 Painel (pergunta 8)
- (i) **Leitura no detalhe do caso** (frente 142) sob grant `chat_evidence`
  (kind 'R', VIEW, **sem bootstrap**, como `media_original`), cada leitura
  auditada (166); sem escrita, sem responder.
- (ii) Sob o VIEW de `reports`, auditado.
- (iii) Nunca no painel (só via dual-control 45).
- Moderação de mensagem (ocultar mensagem individual) — nesta frente ou
  fica para "sinalizar conteúdo" (161)?

### 5.8 Legal Gate (pergunta 9)
`chat.masked` nasce em `PENDING_WIRING` e é cabeada na C1 (i), ou o chat
não é capacidade regulável (ii)?

### 5.9 Limites (pergunta 10)
Rate limit por thread e por conta (ex. 30 msg/min), tamanho máx. 1000,
sem mídia, sem edição/apagamento pelo autor (append-only como a
timeline) — aceitar como fixo (i) ou revisar (ii)?

## 6. Decisões registradas

Texto integral no [VGR-plano.md](../decisions/VGR-plano.md), seção
"Chat mascarado denunciante ↔ helper (rodada 12)".

- **168** — três fases C1 → C2 → C3, liberação por fase.
- **169** — só identidade roteável conversa; helper sem conta avisado
  antes de oferecer; denunciante anônimo via `x-client-key`.
- **170** — cada lado vê o que a oferta mostrava; tokens opacos por
  (thread, participante); denunciante nunca mostra nome.
- **171** — anti-contato bloqueado no servidor (`CONTACT_NOT_ALLOWED`),
  espelho em `vgr_validators`; máx. 1000 chars.
- **172** — polling com cursor; fila offline com `clientKey`.
- **173** — thread na 1ª mensagem; resolvido/oculto fecham escrita;
  congelado segue; purge zera texto.
- **174** — timestamps degradados por tier; sem "visto".
- **175** — painel lê sob `chat_evidence` (R, sem bootstrap), auditado;
  sem escrita; sem ocultar mensagem.
- **176** — capacidade `chat.masked` no Legal Gate, cabeada na C1.
- **177** — 30 msg/min/thread, 1000 chars, sem mídia, append-only (env).

## 7. Fora de escopo (já claro sem pergunta)

- Push/notificação proativa (11) — visão.
- Mídia no chat (54) — anexos continuam no report.
- Chat em grupo / entre helpers (55).
- Tradução automática, IA de moderação de texto.
- Chat do botão de pânico (51/62–65) — frente própria.

## 8. Pendências (rodada 12 — chat mascarado)

**Nenhuma.** Itens 1–10 resolvidos em 2026-09-03 pelas decisões 168–177.

## 9. Critérios de sucesso

1. Nenhum payload do chat contém `accountId`, e-mail, `clientKey` ou
   nome de quem é anônimo; em tier high, nenhum nome — teste por rota.
2. Mensagem com telefone/e-mail/URL/handle é recusada com `code` próprio;
   o app antecipa com a mesma regra (teste espelhado, 154).
3. Denunciante sem conta conversa pelo `x-client-key`; helper sem conta
   recebe o aviso antes de oferecer (169).
4. Resolver/ocultar fecha a escrita; purge zera o texto; congelado não
   expira — testes no ciclo de vida.
5. Painel lê só com o grant próprio e cada leitura grava auditoria.
6. Gate `chat.masked` fail-closed em jurisdição real (451).
7. Suítes verdes (API, mobile, admin, guards 133), feature docs
   `api/docs/feature/chat.md` e `app/docs/feature/chat.md`, spec 003/004
   emendadas onde divergirem (36/37), `VGR-RESUMO.md` §4.
