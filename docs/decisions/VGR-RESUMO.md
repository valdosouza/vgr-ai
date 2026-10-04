# VGR — Resumo executivo do projeto

> **Propósito deste documento**: porta de entrada para quem (pessoa ou IA) chega ao
> projeto. Lê-se este resumo primeiro e segue-se aos documentos detalhados só
> quando a frente em questão exigir. Evita reler as 2.200+ linhas do
> [VGR-plano.md](VGR-plano.md) a cada sessão.
>
> **Atualizado em**: 2026-10-04. Se a data estiver distante, confirme o estado
> das frentes no log de decisões antes de confiar nas seções de status.

---

## 1. O que é o produto

App (Flutter, Android/iOS) que cria **vínculo entre pessoas para ajuda mútua**,
disparado por uma **denúncia** de algo acontecendo. Quem está perto vê e escolhe
como ajudar (presença, repasse a autoridades, divulgação, apoio remoto,
contribuição). **Recompensa é opcional e flexível** (decisão 1), modelada como
Promessa de Recompensa do Código Civil (decisão 30). Proteção contra retaliação
é requisito de design de primeira ordem (decisões 6, 40, 41, 55).

Conceito completo: [VGR-plano.md](VGR-plano.md), seções "Contexto" a
"Identificação entre as partes" (decisões 1–12).

## 2. Princípios que valem para TODO código novo

Estes são os invariantes — violar qualquer um exige decisão nova registrada:

1. **Anonimato é social, não forense** (23): a interface esconde identidade;
   a plataforma sempre registra responsabilização (IP, log oculto).
2. **Posição exata nunca sai da API** (135): degradação por RiskTier acontece
   no servidor (grade, baldes de tempo).
3. **Custódia zero** (84): dinheiro nunca toca conta do VGR — split pelo PSP;
   proibido para sempre: carteira, saldo, ledger de fundos, retenção.
4. **Legal Gate fail-closed** (76–79, 103–109): capacidade sem regra ativa é
   bloqueada em jurisdição real; `SANDBOX` inverte o default. Capacidade nova
   nasce em `PENDING_WIRING` e é removida ao cabear.
5. **Specs são vinculantes, emenda antes de divergir** (36, 37): código que
   revela spec errada → parar, emendar com nota "Amended", retomar.
6. **Erro da API só em inglês; o `code` é o contrato de i18n** (80, 83).
7. **Dois planos de auth nunca cruzados** (119): painel (`aud: admin`) × app
   (`aud: app`), rejeição cruzada nos middlewares.
8. **Nenhum widget Flutter direto em tela — tudo `Vgr*`** (133), guardado por
   teste, replicado no mobile e no admin.
9. **Segurança — regras permanentes de review** (110): log nunca recebe
   senha/token/body/IP/localização; SQL parametrizado; endpoint nasce com
   `requirePrivilege`; segredo só em env.
10. **"A denúncia nunca espera"** (123): identidade/fricção só quando o caso
    escala; fila offline (28) para tudo que pode subir depois.
11. **Nenhum SDK de provedor externo direto em módulo de domínio — sempre
    por *port* em `shared/`, implementação trocável por config** (143):
    mesma lógica da 133, aplicada à API (`BlobStore`, `PaymentRail`, e agora
    `LegalAssessmentProvider` da L2, decisão 144).

## 3. Método de trabalho

- **Execução interativa, fase a fase** (38): Valdo libera cada fase com
  **"pode seguir"**. Nunca avançar fase sem essa liberação.
- **Decisões novas SEMPRE via decision-rounds**, numeração contínua no
  [VGR-plano.md](VGR-plano.md). ⚠️ **Reler o log inteiro antes de numerar** —
  sessões paralelas já causaram colisão (caso 93/102).
- Sessões paralelas: claim na memória antes de começar fase; baixa com commit.
- API primeiro quando o app depende de endpoint inexistente (66).
- Stack (15–17): Flutter workspace (`flutter_modular` + `bloc` + `dartz`),
  packages próprios `core`/`vgr_widgets`/`vgr_validators`; API Express/TS
  modular, MySQL `tb_` + soft delete; código/comentários/docs técnicas em
  inglês; docs de decisão em português. Estrutura espelha setes-app/setes-api
  (`D:\Gestao2027`), sem reaproveitar pacotes.
- Repositórios: `D:\ProjetoVGR\app` (mobile + admin no mesmo workspace) e
  `D:\ProjetoVGR\api`.

## 4. Frentes — status e onde está o detalhe

| Frente | Decisões | Status (2026-08-19) | Plano detalhado |
|---|---|---|---|
| Conceito / fluxo end-to-end | 1–67 | Fechado | [VGR-plano.md](VGR-plano.md) |
| Controles administrativos (permissões, menu, i18n, kind 'R') | 68–75, 80, 83, 93 | **Entregue** (fases 0–5 + rodada 1 zerada) | [plano-controles-administrativos.md](../plans/plano-controles-administrativos.md), [plano-erro-i18n.md](../plans/plano-erro-i18n.md) |
| Legal Gate (bloqueio por jurisdição) | 76–79, 103–109, 143–146 | L0+L1 na API; **L3 (telas admin) entregue em 2026-08-19**; **rodada 2 fechada por completo em 2026-08-20**; só resta a escolha comercial do provedor da L2 | [plano-legal-gate.md](../plans/plano-legal-gate.md) |
| Trilho de pagamento (recompensa) | 81–102 (menos 93), 147–150 | Rodada 3 zerada; **só Pix** (95); conector `PaymentRail`+Asaas codado (candidato, não decisão 59); **domínio Reward R0 codado em 2026-08-20** (147 fixou recebedores na reserva); **onboarding do helper (API) + disciplina completa da mediação entregues em 2026-08-21** (148: duplo controle sempre; 149: janela de contestação antes de executar; 150: critérios versionados carimbados na reserva); **tela de painel da mediação entregue em 2026-08-21**; **tela mobile do onboarding do helper entregue em 2026-08-21** (fecha o item (e) — só falta ligar de outros pontos do app, se surgir necessidade); roteiro + e-mail ao Asaas prontos ([roteiro](../plans/roteiro-perguntas-asaas.md), [e-mail](../plans/email-asaas.md) — falta Valdo enviar) — chargeback/job de expiração deliberadamente fora | [plano-psp-requisitos.md](../plans/plano-psp-requisitos.md), [plano-garantia-recompensa.md](../plans/plano-garantia-recompensa.md), [payment-rail.md](../../api/docs/feature/payment-rail.md), [reward.md](../../api/docs/feature/reward.md), [reward-onboarding.md](../../app/docs/feature/reward-onboarding.md) |
| Segurança de software | 110–118 | S1–S6 entregues; API e app em contrato | [plano-seguranca.md](../plans/plano-seguranca.md) |
| Auth de usuários do app | 119–125, 151–152 | API entregue (`/app-auth`, dois planos); **rodada 6 itens 2–3 fechados em 2026-08-22** (151 verificação de e-mail, 152 adapters sociais adiados) — telas mobile de cadastro/login/verificação/sair entregues junto; **login Google entregue ponta a ponta em 2026-08-22** (API + botão no app mobile, só Android — iOS sem client OAuth ainda); resta o item 1 (provedor de OTP, comercial) | [plano-auth-usuarios.md](../plans/plano-auth-usuarios.md), [app-auth.md (API)](../../api/docs/feature/app-auth.md), [app-auth.md (mobile)](../../app/docs/feature/app-auth.md) |
| Imagens/mídia | 126–132 | M1+M2+M3 entregues (plano inteiro); aberto só o provedor S3 pago (adiado até haver volume) | [plano-imagens.md](../plans/plano-imagens.md) |
| Design system | 133 | Vigente (guarda por teste) | — |
| Chat mascarado denunciante ↔ helper | 168–177 | **Entregue por completo em 2026-09-03** — C1 API (`8af91a8`, `b13ed6a`), C2 mobile (`7c75d4f`), C3 painel (api `42f8408`, app `cdcc478`); migrações 043–044 aplicadas em dev. Fora: push (11), mídia no chat, ocultar mensagem individual (com "sinalizar", 161) | [plano-chat.md](../plans/plano-chat.md), [chat.md (API)](../../api/docs/feature/chat.md), [chat.md (mobile)](../../app/docs/feature/chat.md) |
| Apontamentos de direção (22, 26, 27) | 200–207 | **Entregue por completo em 2026-09-04** — DS1 API (`ed242db`: migração 047, capacidade `location.tracking` cabeada, elegibilidade por categoria fixa no código, piso de 5 apontamentos antes de expor), DS2 mobile (app `b6a15a7`: picker de bússola no detalhe, estimativa também no item do feed, `Direction` promovido a `packages/core`); DS3 painel vazia por decisão | [plano-direction-sightings.md](../plans/plano-direction-sightings.md) |
| Botão de pânico (51, 62–65) | 190–199 | **Entregue por completo em 2026-09-04** — PP1 API (`d74309a`: migração 046, correção de plano do pedido de respondedor, `panic.dispatch` cabeada), PP2 mobile (app `5cdb6d3`: botão no feed, tela de acionamento, inbox do respondedor com polling, pedido de autorização agora alcançável); PP3/PP4 ficam vazias (193/194 tiraram contato de confiança e modo ativado do escopo) | [plano-panico.md](../plans/plano-panico.md) |
| Rating de helpers pelo denunciante (48) | 178–189 | **Rodada 13 fechada em 2026-09-03**; **Entregue por completo em 2026-09-04** — RT1 API (api `ee029bc`), RT2 mobile (app `0035867`: botão de encerrar denúncia, avaliação por oferta na própria tela de detalhe, "minha reputação" na conta, widget `VgrRating` novo), RT3 painel (api `b2388a9`, app `5a9c155`: nota por oferta no detalhe do caso, sob a interface `reports` já existente, sem grant novo) | [plano-rating.md](../plans/plano-rating.md) |
| Busca / moderação / estatísticas do painel (frente 142) | 158–167 | **Entregue por completo em 2026-09-02** — B1 busca+detalhe, B2 moderação, B4 estatísticas (k=5), B3 fila proativa, B5 trilha de auditoria (api `1623c90`/`c9e74b8`/`c5649d1`/`cc2a0b3`/`8cb76c5`, app `9f86945`/`45eb123`/`cd6c376`/`9952c63`/`30b3195`). Migrações 038–042 aplicadas em dev em 2026-09-03. Fora: "sinalizar conteúdo" no app (161), mapa de calor (164), widget de imagem autenticado no painel web | [plano-moderacao-painel.md](../plans/plano-moderacao-painel.md), [report-moderation.md (API)](../../api/docs/feature/report-moderation.md), [report-moderation.md (admin)](../../app/docs/feature/report-moderation.md), [admin-audit.md](../../api/docs/feature/admin-audit.md) |
| Validadores compartilhados do app (`vgr_validators`) | 153–157 | **Entregue em 2026-09-02** (rodada 10 fechada e executada no mesmo dia): API com dígito verificador de CPF/CNPJ (`d593fd0`), pacote real + `VgrTextField.mask` + onboarding migrado (app); guard de validação inline adiado (156) | [plano-validadores.md](../plans/plano-validadores.md), [validators.md](../../app/docs/feature/validators.md) |
| Oferta de ajuda com vários tipos | 208–214 | **Rodada 16 fechada em 2026-09-11**; **HT1 API executada em 2026-09-11** (migração 049: tabela filha `tb_help_offer_type`, coluna antiga removida; `helpTypes: []` no POST e nas visões; `PUT /app-help-offers/:id/types` para o helper trocar o conjunto em denúncia aberta); **HT2 mobile executada em 2026-09-19** (bloc com conjunto, checkboxes múltiplos, "Alterar tipos de ajuda" no detalhe do participante; adendo HT1 na API: facet `myOffer` na visão de participante); **HT3 painel executada em 2026-09-19** (entidade e linha da oferta com `helpTypes`); **FRENTE COMPLETA** | [plano-oferta-multitipo.md](../plans/plano-oferta-multitipo.md) |
| Painel admin no modelo setes (shell, fábrica CRUD, paginação) | 215–222 | **Rodada 17 fechada em 2026-09-21**; **PS1 shell executada em 2026-09-21** (HomeModule com RouterOutlet, duas colunas, drawer, Sair, `VgrPage`); **PS0 API executada em 2026-09-21** (api `cecc1e0`: paginação opcional e compatível nas listas que crescem); **PS2 fábrica executada em 2026-10-04** (app `f7ebbd7`: `RegisterBloc<T, D>` genérico + `RegisterScreen`, ponte de feedback guardada por teste, `PagedResult` no core, piloto `privileges` + `users`; corrigido de passagem o `locale` apagado ao editar usuário); **PS3 migração executada em 2026-10-04** (app `80cf51d`…`86fe644`: todas as telas na fábrica ou na ponte, Legal Gate e respondedores paginados, um pager só, guarda da 221 estrita; achados e corrigidos 4 telas que caíam em erro ao recusar uma ação e o dual-control que perdia a solicitação em andamento); **PS4 docs executada em 2026-10-04** (app `1314904`: checklist `ADMIN-SCREENS.md`, `ARCHITECTURE.md` § ADMIN PANEL, inventário em `admin-panel.md`); **FRENTE COMPLETA** — 2 pendências de decisão no §9 do plano (⚠️ dual-control com aprovador digitado; `locale` na API) | [plano-painel-modelo-setes.md](../plans/plano-painel-modelo-setes.md), [ADMIN-SCREENS.md](../../app/docs/adr/ADMIN-SCREENS.md) |
| Duplo controle de verdade (corrige a implementação da 45) | 223–229 | **Rodada 18 fechada em 2026-10-04**; **DC1 API executada em 2026-10-04** (api `ea3184f`: migração 050 — solicitante e aprovador da sessão, pedido + 1 aprovação de OUTRA pessoa, CHECK de duas pessoas no banco, solicitações antigas anuladas `void`, auditoria, 404 na entrada inexistente, lista paginada com nomes; validada em MySQL 8.0 e MariaDB 10.11); **DC2 painel aguarda "pode seguir"** — até lá a tela antiga não lê as linhas novas. Revelação (decifrar) fora: rodada própria após revisão jurídica (228) | [plano-dual-control.md](../plans/plano-dual-control.md), [dual-control-access.md (API)](../../api/docs/feature/dual-control-access.md) |
| Denúncia (Report) | 134–142 | **Entregue** (R1–R4 na API + A1–A3 no mobile + P1 no painel); busca/moderação/estatísticas do painel = frente própria (142) | [plano-denuncia.md](../plans/plano-denuncia.md), [handoff-A1-app-denunciar.md](../plans/handoff-A1-app-denunciar.md) |

Especificação DDD vinculante: `api/docs/specs/vgr/` (tactical design + cenários
de teste). Feature docs do que já existe: `api/docs/feature/*.md` e
`app/docs/feature/*.md`.

## 5. Fora do MVP (visões registradas — não implementar sem rodada)

Previsão de trajetória com push proativo (11) · validação de cadastro policial
(12) · sinalização "possível armadilha" (43) · despacho automático a
autoridades (53) · voucher anônimo (61 — **proibido** nas críticas pela 82) ·
profissionalização de helpers (125) · avatar (127) · vídeo/áudio (132) ·
convite de equipe por e-mail (75) · trilho de pagamento próprio
(`reward.intermediation.own`, 81/99) · **Nostr/descentralização — descartado
por completo em 2026-08-19** (não repropor; ver memória `vgr-nostr-descartado`).

## 6. Pendências vivas (o que pode bloquear)

1. **Escolha do PSP** (59): comercial, com critérios fechados — split N
   recebedores (30c), comprovante não nomeia recebedor (82), payout sem o
   denunciante conhecer o helper, retenção Pix fora de conta do marketplace
   (B1) e com prazo máximo conhecido (D1). Se nenhum PSP passar no B1: escolher
   entre não ter selo de garantia ou revisar a decisão 84.
2. **Provedor de OTP** (rodada 6, item 1 — só este resta): envio de
   telefone/WhatsApp, comercial, mesmo formato da 59. Verificação social
   (item 3) e verificação de e-mail (item 2) fechadas em 2026-08-22
   (decisões 151–152) — adapters sociais adiados até haver credencial
   OAuth real, não é mais pendência de decisão.
2b. **Provedor de IA da L2** (144): critério fechado (grounding > preço),
    falta a escolha comercial — mesmo formato de pendência do item 1 e 2.
3. ~~Critérios de "respondedor autorizado"~~ **FECHADO em 2026-09-04**
   (decisão 190): sem regra codificada, julgamento humano livre —
   `criteria_notes` livre já é o desenho final, não pendência de decisão.
4. **Textos jurídicos** com advogado antes do lançamento (25, 30, 45, 57) —
   via Legal Gate (77), não bloqueiam desenvolvimento.
5. ~~Risco aberto no código~~ **FECHADO em 2026-08-19**: o veto da 58/82
   está no `monetization-config` (leitura: regra efetiva de categoria
   high nunca contém `peer_to_peer`; escrita: 422 explícito) — a
   extração de `shared/risk/risk-tier` que faltava veio com a R2.
5b. ~~Gap 4 da auditoria TDD~~ **FECHADO em 2026-09-02** (decisões
    153–157 executadas; ver §4). Fica registrado para o futuro: a opção B
    (módulo `api/src/shared/validation` + guard de validação inline em
    tela, 156) reabre quando surgir o segundo formulário com campo de
    formato.
5c. **Consolidação + primeiro teste manual ponta a ponta (2026-09-06)**: flake do
    CI do admin corrigido; helpers duplicados da API extraídos para `shared/`
    (api `ee1b1cc`); `MyReportsStore` promovido a `app/shared/` e `RATING_CLOSED`
    com frases por motivo (app `88301ea`). O teste manual no navegador achou e
    corrigiu: CORS sem `x-client-key` (api `a89e110`), 500 no pânico por
    respondedor sem conta + FK que faltava (api `660be3d`, migração 048), Jest
    varrendo worktrees em `.claude/`. Receita e achados: memória
    `vgr-teste-manual-web`. Fluxos identificados (helper com conta, painel)
    dependem de login manual de Valdo.
5d. **Dual-control com aprovador digitado (achado em 2026-10-04, PS4)** —
    rodada 18 (223–229); **corrigido na API pela DC1** (api `ea3184f`). Falta
    a **DC2 painel** (aguarda "pode seguir"): a tela atual ainda fala o
    contrato antigo e não lê as linhas novas. Detalhe:
    [plano-dual-control.md](../plans/plano-dual-control.md).
5e. **`locale` no update de usuário (API)**: ausente vira `null`; o painel
    já contorna reenviando — decidir se a API preserva.
5f. **Migração 049 só roda em MariaDB (achado em 2026-10-04, DC1)**:
    `DROP CONSTRAINT IF EXISTS` / `DROP COLUMN IF EXISTS` não existem no
    MySQL 8.0 — lá a 049 falha e trava as seguintes. O dev é MariaDB (a
    cadeia 001–050 roda inteira em MariaDB 10.11), mas a stack diz "MySQL".
    Decidir o motor de produção; se for MySQL, a 049 precisa de forma
    portável (sem `IF EXISTS`).
6. Frentes ainda não abertas: "sinalizar conteúdo" pelo usuário no app
   (161). Direction sightings (22/26/27) **aberto em 2026-09-04** (rodada
   15, decisões 200–207; DS1+DS2 entregues, DS3 vazia) — fecha a promessa
   da 189 (peso de reputação fica fora, deliberadamente). Rating (48) **completo em
   2026-09-04** (rodada 13, decisões 178–189; RT1+RT2+RT3 entregues).
   Pânico (51/62–65) **aberto em 2026-09-04** (rodada 14, decisões
   190–199; **completo**, PP1+PP2 entregues, PP3/PP4 vazias) — critério de respondedor fechado sem
   subsistema novo (190), contato de confiança e modo ativado ficam de
   fora (193/194).
   Chat mascarado (54) **completo em 2026-09-03** (rodada 12, decisões
   168–177). Busca/moderação/estatísticas do painel
   (142) **completa em 2026-09-02** (rodada 11, decisões 158–167). Recompensa (domínio Reward) tem R0
   codado em 2026-08-20 (ver §4) — mediação e onboarding do helper
   (API + mobile) entregues em 2026-08-21; só chargeback e job de
   expiração ficam deliberadamente fora, aguardando D1 com o PSP.

## 7. Mapa da pasta `AI/`

- `AI/docs/decisions/VGR-plano.md` — **log mestre de decisões** (fonte da
  verdade de negócio; numeração contínua).
- `AI/docs/plans/*.md` — plano executivo de cada frente (linkados na tabela §4).
- `AI/docs/categoria/` e `AI/docs/Objetos/` — ícones do app anterior, semente
  da taxonomia de dois eixos (decisões 3, 140).
- `AI/vgr-kit/` — harness de agentes/skills (decision-rounds, scope-refinement,
  tdd-orchestrator, project-memory etc.), independente do produto.
