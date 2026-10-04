# Plano — Botão de pânico (decisões 51, 62–65)

> **Rodada 14 — FECHADA em 2026-09-04** (rodada 0 e rodada 1 no mesmo
> dia). Decisões **190–199** registradas no
> [VGR-plano.md](../decisions/VGR-plano.md). Execução PP1 → PP2 → PP3
> (se houver) → PP4 (se houver), cada fase liberada por "pode seguir"
> (38). **PP1 executada em 2026-09-04** (api `d74309a`); **PP2 executada
> em 2026-09-04** (app `5cdb6d3`). **FRENTE COMPLETA** — PP3 não
> construída (194 tirou o modo avançado do escopo) e PP4 confirmada
> vazia (a fila de aprovação já existia e não mudou). Frente escolhida
> por Valdo em 2026-09-04,
> entre as três que restavam (pânico, direction sightings, sinalizar
> conteúdo).

---

## 1. Contexto

As decisões 51 (rodada original) e 62–65 (correção posterior) desenharam
o pânico como **funcionalidade independente do fluxo de denúncia**
(62), acessível a qualquer momento por um menu, com **dois níveis de
acessibilidade** — padrão (sem configuração prévia) e ativado/em destaque
(opt-in, para quem antecipa risco, 63) —, **destinatário configurável em
dois modos não exclusivos** — pool de Respondedores Autorizados da
plataforma e/ou contato pessoal de confiança (64) —, e um **uso "a
frio"** que vai direto pro pool sem exigir configuração (65). A decisão
51 já fixa que "cada respondedor autorizado recebe a mensagem e a
distância até a ocorrência", e a **decisão 52 ficou deliberadamente
pendente**: os critérios de quem pode virar respondedor autorizado nunca
foram fechados — "não bloqueia o desenho da estrutura, só bloqueia o
lançamento real do recurso até os critérios existirem". Essa pendência
é reaberta nesta rodada.

**O que já existe e condiciona o desenho (evidência, 2026-09-04):**

| Peça | Estado | Consequência para o pânico |
|---|---|---|
| Pool de respondedores (`api/src/modules/panic/responder-pool.*`) | **Pré-requisito já construído**: `tb_responder_pool_membership` (migração 012: `user_id`, `status pending/approved/denied`, `criteria_notes` texto livre — o próprio SQL comenta "pending decision 52's resolution"), `POST .../responder-pool` (pedir), `GET` (listar pendentes, grant `panic_responders`), `PUT .../:id/resolve` (aprovar/negar, mesmo grant) | O mecanismo de autorização já existe; falta só o CRITÉRIO (52) — o resto é reaproveitável |
| **Achado a corrigir**: as três rotas do pool estão montadas em `router.use('/panic/responder-pool', ...)`, dentro do roteador `/api`, que é **globalmente protegido por `authMiddleware` com `audience: Audiences.ADMIN`** (`app.ts:148`, `auth.middleware.ts:42`). Um usuário do app (JWT `aud: app`) não consegue chamar `POST /api/panic/responder-pool` — o pedido de autorização, que é ação do HELPER, está hoje inalcançável pelo próprio app | Bug de posicionamento de plano (119), não decisão de negócio — corrigido durante a construção desta frente (mover o `POST` para o plano do app, `/app-panic/responder-pool`; `GET`/`PUT resolve` continuam no `/api`, corretos como estão) |
| Painel admin (`apps/admin/lib/.../modules/panic-responders/`) | **Já existe**: fila de pendentes, aprovar/negar por botão, grant `panic_responders` (`interface_routes.dart:18`) | Fica como está — só o critério de julgamento muda, não a tela |
| `PanicAlert` / `AlertRecipient` / `TriggerPanicAlert` (spec `003`) | **Nenhum código** — zero tabela, zero módulo além do pool. Spec: `PanicAlert.trigger()` lança erro se `recipients.length === 0` após aplicar o pool como default; `AlertRecipient` é união discriminada `responder_pool \| trusted_contact`; evento `PanicAlertTriggered {alertId, triggeredBy, recipients[], position}`, consumido por "Notification delivery (**out of MVP scope beyond in-app**)" | O agregado inteiro nasce nesta frente. A anotação do próprio evento já aceita entrega só em app (sem push) como MVP |
| Contato de confiança (64, modo 2) | **Nada existe** — nenhuma tabela/coluna para contato pessoal em `tb_user_account` ou qualquer outra; comentário da migração 027 é explícito: "no contacts (minimization, decision 110)" | Modo greenfield total — decide-se aqui se entra nesta rodada |
| Entrega sem push | Confirmado: sem infra de push/SSE/websocket em lugar nenhum do projeto. Dois precedentes de polling: feed (`GET /app-feed`, paginação por página) e chat (`GET .../messages?after=<id>`, cursor, decisão 172 — "push fica visão, SSE/websocket ficam para quando houver volume") | O pânico precisa do mesmo tipo de solução — decisão de qual padrão usar e onde |
| Geolocalização (`LocationGateway.currentPosition()`) | **Só um tiro** — `Future<GeoPoint>`, sem `Stream`/watch. Nenhum gateway contínuo existe | "Geolocalização contínua" (linguagem da 62–65) exige gateway novo SE o alerta for uma sessão viva; um alerta de posição única não exige nada novo |
| Degradação de distância por tier | `shared/geo/degrade.ts`: `DISTANCE_STEP_BY_TIER` (arredondamento em km, já distinto da degradação de posição bruta `GRID_BY_TIER`) — parece feito sob medida para "só a distância", exatamente o que a 51 pede | Reaproveitável direto, sem desenhar nada novo |
| Legal Gate | `Capabilities.PANIC_DISPATCH = 'panic.dispatch'` já declarada, em `PENDING_WIRING` (nunca chamada) | Cabeia nesta frente, mesmo padrão da 176/188 |
| Migrações | Última: `045_helper_rating.sql` | Próxima: **046** |
| App mobile | **Nada** — nenhum menu, tela, bloc ou módulo com "panic"/"responder" (fora um falso positivo de string) | Frente inteira do lado mobile é greenfield |

## 2. Invariantes que a frente NÃO pode tocar

- Pânico continua **independente do fluxo de denúncia** (62) — não uma
  pergunta na tela de categoria.
- Identidade do respondedor nunca é exposta a quem aciona o pânico —
  mesmo princípio de anonimato/responsabilização das decisões 6/23/55/60
  aplicado aqui: a plataforma sempre sabe quem é quem, a interface nunca
  mostra a quem não deve.
- Posição exata nunca sai da API (135) — o que o respondedor recebe é
  distância degradada por tier, nunca lat/lng bruto, mesmo padrão da
  denúncia.
- Nenhum despacho automático a autoridades (53) — o MVP é notificação
  aos respondedores autorizados, sem promessa de acionamento automático.
- Erro só em inglês com `code` (80/83); enforcement no servidor (72/110);
  endpoint nasce com gate/privilégio; log sem IP/localização exata.
- Dois planos de auth nunca cruzados (119) — a correção do item acima
  aplica exatamente essa regra ao pedido de autorização.
- Nenhum widget Flutter direto (133); validação via `vgr_validators`
  onde houver campo de texto.

## 3. Objetivos (confirmados pelas decisões 190–199)

1. Usuário aciona o pânico a qualquer momento por um menu, sem
   configuração prévia — e um alerta chega a pelo menos um destinatário
   (65), nunca falha silenciosamente por falta de destinatário.
2. Usuário pode, antecipadamente, ativar o modo em destaque e configurar
   quem recebe (63/64), dentro do escopo que a rodada decidir.
3. Usuário pode solicitar autorização de respondedor; administrador
   julga por um critério agora existente (fecha 52); a UI de aprovação
   já pronta continua funcionando sem mudança.
4. Respondedor autorizado recebe o alerta com distância degradada,
   dentro do app, sem push (mesma aceitação já registrada no evento da
   spec).
5. Nenhum dado de posição exata ou identidade indevida atravessa a API;
   capacidade no Legal Gate; testes; docs.

## 4. Fatiamento (decisão 199 — PP1 → PP2 → PP3/PP4 condicionais)

| Fase | Entrega provável | Depende de |
|---|---|---|
| **PP1 — API** — **EXECUTADA em 2026-09-04** (api `d74309a`; 97 suítes/1001 testes, era 93/946; migração 046 aplicada em dev). Corrigido o bug de plano do pool de respondedores (`POST` movido pra `/app-panic/responder-pool`); agregado novo em `src/modules/panic/panic-alert.*`; cooldown só para quem tem conta (anônimo sem identidade estável entre tentativas); `panic.dispatch` já estava semeada pela migração 022, só cabeada agora | Migração 046 (`tb_panic_alert`, talvez `tb_panic_alert_recipient` conforme a 3); correção de plano do `POST .../responder-pool` para `/app-panic/responder-pool`; critério de respondedor (1) aplicado no julgamento admin (pode ser só documentação + `criteria_notes` continuando livre, sem mudança de schema); `POST /app-panic/alert` (aciona), `GET /app-panic/alerts` (inbox do respondedor, polling), `POST /app-panic/alerts/:id/resolve`; capacidade `panic.dispatch` cabeada | — |
| **PP2 — Mobile (padrão)** | Menu → botão de pânico, confirmação, aciona; tela "Alertas" do respondedor (polling, distância); fluxo de pedido de autorização de respondedor (agora alcançável) | PP1 |
| **PP3 — Mobile (avançado)** | **Não construída** (194 tirou o modo ativado/em destaque do escopo) — fica como visão futura | — |
| **PP4 — Painel** | **Vazia, confirmado ao final da PP2** — a fila de aprovação já existia e não mudou (190 manteve o julgamento livre); nenhuma tela nova necessária | — |

## 5. Alternativas que estavam em cima da mesa (escolhas nas decisões 190–199)

### 5.1 Critério de respondedor autorizado (pergunta 1 — fecha a 52)
- (i) **Sem critério codificado — julgamento humano livre**, exatamente
  como o pré-requisito já constrói (`criteria_notes` texto livre,
  decisão do administrador caso a caso). Fecha a pendência sem
  subsistema novo.
- (ii) Piso automático antes da fila humana (ex.: e-mail verificado, N
  dias de conta) + julgamento humano por cima.
- (iii) Só por convite — administrador convida, sem autoatendimento
  (o `POST` de pedido deixaria de fazer sentido).

### 5.2 Um alerta ou uma sessão viva (pergunta 2)
- (i) **Um tiro**: posição única no acionamento, mensagem fixa, pronto —
  MVP pequeno, sem gateway de geolocalização novo.
- (ii) **Sessão viva**: o alerta fica "ativo", a posição atualiza
  periodicamente (ex. a cada N segundos enquanto a tela está aberta,
  mesmo padrão do polling) até ser resolvido/cancelado — mais fiel à
  "geolocalização contínua" do texto das decisões 62–65, mas exige
  gateway de posição em stream (novo) e mais estado no servidor.

### 5.3 Entrega ao respondedor (pergunta 3)
- (i) **Tela própria "Alertas"**, polling por cursor como o chat
  (`after=<id>`, intervalo curto só com a tela aberta, decisão 172 como
  precedente direto).
- (ii) O alerta aparece embutido em alguma tela já existente (ex. feed) —
  mistura conceitos, não recomendado.

### 5.4 Contato de confiança — escopo desta rodada (pergunta 4)
- (i) **Fora desta rodada** — só o modo pool de respondedores (64,
  primeira metade) sai agora; contato pessoal fica registrado como
  próxima rodada. Evita depender de um provedor de SMS/e-mail externo
  (mesma família de pendência comercial do OTP, ainda em aberto) e de
  desenhar consentimento LGPD pra terceiro que pode nem ter conta.
- (ii) Contato de confiança **é uma conta VGR já existente** (busca por
  conta, sem dado de contato externo) — entrega pela mesma tela de
  alertas do respondedor, sem SMS/e-mail; menor escopo que (iii).
- (iii) Contato de confiança é **um número de telefone qualquer**,
  entregue por SMS — precisa de provedor comercial (mesmo tipo de
  decisão pendente do OTP), maior escopo.

### 5.5 Modo ativado/em destaque — escopo desta rodada (pergunta 5)
- (i) **Fora desta rodada** — só o botão padrão (uso a frio, 65) sai
  agora; o modo opt-in com pré-configuração de destinatário fica para
  quando o contato de confiança (se aplicável) também estiver pronto.
- (ii) Entra nesta rodada, mas com destinatário restrito ao pool
  (nenhuma configuração de contato de confiança ainda, mesmo se a
  pergunta 4 escolher (i)) — só o botão fica mais visível/acessível.
- (iii) Entra completo, amarrado ao que a pergunta 4 decidir.

### 5.6 Distância mostrada ao respondedor (pergunta 6)
- (i) **Reaproveita `DISTANCE_STEP_BY_TIER`** (`shared/geo/degrade.ts`) —
  já existe, já é a régua certa (arredondamento em km por tier).
- (ii) Régua nova, mais fina ou mais grossa que a dos reports.

### 5.7 Conteúdo da mensagem do alerta (pergunta 7)
- (i) **Modelo fixo** ("Fulano acionou o botão de pânico, a X km de
  você") — sem texto livre do usuário. Consistente com a 65 ("sem
  exigir mais informação do usuário no momento do clique"); evita abrir
  uma superfície nova de moderação/filtro de contato.
- (ii) Texto livre opcional além do modelo fixo — mais contexto, mas
  precisa do mesmo filtro anti-contato (171) e de decisão sobre
  moderação/retenção desse texto.

### 5.8 Ciclo de vida / quem resolve (pergunta 8)
- (i) **Só quem acionou resolve** ("estou seguro agora") — mais simples,
  evita um respondedor encerrar um alerta que não é dele.
- (ii) Quem acionou OU um respondedor que atendeu pode resolver (com
  motivo).
- (iii) Sem resolução — o alerta só expira por tempo (menos controle,
  não recomendado para algo de segurança).

### 5.9 Anti-abuso (pergunta 9)
- (i) **Cooldown simples**: não é possível abrir um novo alerta enquanto
  o anterior do mesmo usuário está ativo (evita duplicar clique/spam
  básico) — sem sistema de detecção de fraude.
- (ii) Sem nenhum limite — qualquer clique cria um alerta novo.
- (iii) Limite por período (ex. N por dia) — mais fricção, mais
  complexidade, risco de bloquear uma emergência real repetida.

### 5.10 Fatiamento (pergunta 10)
- (i) **PP1 API → PP2 mobile padrão → PP3 mobile avançado (se houver) →
  PP4 painel (se houver)**, cada fase por "pode seguir" (38), API sempre
  sem pendência antes da próxima fase ([[metodo-fase-api-sem-pendencia]]).
- (ii) Fatiamento diferente, a propor.

## 6. Fora de escopo (visões registradas, independente das respostas acima)

- Despacho automático a autoridades (53) — já fora do MVP por decisão
  anterior, não repropor.
- Detecção de fraude / "possível armadilha" no pânico (43 é sobre outra
  coisa — sinalização comunitária na denúncia — não confundir).
- Push proativo (11) — mesma visão já registrada em todo o projeto.
- SMS/e-mail para contato de confiança, se a pergunta 4 escolher (i) ou
  (ii) — fica visão para quando o provedor comercial (mesma família do
  OTP) for decidido.

## 7. Critérios de sucesso

1. Um pedido de autorização de respondedor, feito pelo app, chega ao
   administrador e pode ser aprovado/negado pela tela já existente.
2. Um acionamento "a frio" (sem configuração prévia) sempre resolve a
   pelo menos um destinatário — nunca falha por falta de recipiente.
3. Um respondedor autorizado enxerga o alerta com distância degradada
   por tier, nunca posição exata.
4. Capacidade do Legal Gate bloqueada → 451 antes de qualquer
   acionamento gravado.
5. Suítes verdes nos dois repositórios; specs 003/004 emendadas; docs de
   feature nos dois lados.

## 8. Decisões registradas (rodada 14 — 2026-09-04)

Valdo respondeu `1 i | 2 i | 3 i | 4 i | 5 i | 6 i | 7 i | 8 i | 9 i | 10
i` — todas na opção recomendada. Texto integral no
[VGR-plano.md](../decisions/VGR-plano.md), seção "Botão de pânico
(rodada 14)".

| Item | Decisão | Resumo |
|---|---|---|
| 1 | 190 | Critério de respondedor: julgamento humano livre, sem regra codificada (fecha 52) |
| 2 | 191 | Alerta é um tiro único, sem sessão viva |
| 3 | 192 | Tela própria de alertas, polling por cursor (padrão do chat) |
| 4 | 193 | Contato de confiança fica fora desta rodada |
| 5 | 194 | Modo ativado/em destaque fica fora desta rodada |
| 6 | 195 | Distância reaproveita `DISTANCE_STEP_BY_TIER` |
| 7 | 196 | Mensagem em modelo fixo, sem texto livre |
| 8 | 197 | Só quem acionou resolve o alerta |
| 9 | 198 | Anti-abuso: cooldown simples, um alerta ativo por vez |
| 10 | 199 | Fatiamento PP1 → PP2 → PP3/PP4 condicionais |

**Correção aplicada durante a construção, não uma pergunta**: o `POST`
de pedido de autorização de respondedor será movido do plano admin
(`/api`, hoje inalcançável por um usuário do app) para o plano do app
(`/app-panic/responder-pool`) na PP1 — bug de posicionamento de plano
(119), não escolha de negócio.

## 9. ⚠️ Pendências

Nenhuma. Visões deixadas para rodada futura estão no §6.
