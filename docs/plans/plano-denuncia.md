# Plano da denúncia (Report) — VGR

> Data: 2026-08-03 · Status: **rodada 8 ZERADA — decisões 134-142**;
> **R1-R4 EXECUTADAS** (R1-R3 em 2026-08-03, R4 em 2026-08-04) — o lado
> API da frente está completo; **A1 e A2 EXECUTADAS em 2026-08-04** (tela
> de denunciar + feed/detalhe no mobile); **A3 e P1 EXECUTADAS em
> 2026-08-19** — a frente está COMPLETA (R1-R4 + A1-A3 + P1).
> Escopo: núcleo da denúncia — Report + taxonomia, SubmitReport (anônimo e
> autenticado), feed por proximidade (raio dinâmico), HelpOffer,
> edição/resolução/timeline, visibilidade, retenção e o M2 de imagens.
> Fora desta frente (ficam para as próximas): apontamentos de direção
> (tasks 08-10), recompensa/pagamento (14/15/20/30 — frente do trilho),
> chat mascarado (29), botão de pânico (28), avaliação de helper (26).

---

## 1. Ponto de partida

Esta é a frente que todas as outras prepararam. A spec vinculante existe
(`api/docs/specs/vgr/003-api-tactical-design.md`, tasks 01-07/21/24/25 +
`004-api-test-scenarios.md`; mobile em `app/docs/specs/vgr/003-mobile-*`),
e o inventário do que já está construído e testado:

- **Dois planos de auth** (119): `/app-auth` com UserAccount; anônimo sem
  token (32/35) com rastro no accountability log (23, módulo identity).
- **Legal Gate** (103-109): capacidade `report.anonymous` está em
  `PENDING_WIRING` — o teste de partição do catálogo OBRIGA removê-la ao
  cabear o consumidor.
- **Risk config** (46) e **CategoryFormSchema** (47): tier por categoria
  (TTL cache) e validação server-side dos campos de detalhe por categoria.
- **Mídia M1+M3** (126-132): upload anônimo, cifra, blur no ingest,
  retenção por crypto-shredding, leitura auditada no painel. Falta o M2.
- **Scheduler** (90) e job de expiração (131) rodando.
- **App**: design system da decisão 133 (tudo `Vgr*`, guarda por teste),
  fila offline especada (`OfflineQueueService`, decisão 28), i18n.

## 2. Emendas propostas à spec (decisão 37 — emendar antes de divergir)

A tactical design é anterior às decisões 76+ (Legal Gate), 119 (planos),
123 (fricção), 126-132 (mídia) e 133 (design system). Emendas a registrar
na spec antes do código ("Amended — frente denúncia"):

- **E1 — Plano de montagem**: tasks 03/07 dizem `POST /api/reports`; /api
  é o plano do PAINEL (119). As rotas do app montam em **/app-reports**
  (padrão /app-auth, /app-media): submit/feed/detalhe/help-offer; as rotas
  do painel (moderação, busca administrativa) é que vivem em /api com
  `requirePrivilege`.
- **E2 — Taxonomia incompleta**: o `Report` da spec tem só
  `category | freeTag`. A decisão 3 (e o critério de sucesso 1) exige
  **categoria × objeto/sujeito** — `SubjectTag` aparece na spec apenas no
  caso Child (25). Emenda fixada pela decisão 140: dois eixos, **ambos
  obrigatórios** (objeto com opção genérica "other" de um toque — guarda
  da 123), semente canônica em código com liberdade sobre os ícones.
- **E3 — Legal Gate**: `SubmitReport` anônimo consome `report.anonymous`
  (cabear `requireCapability`/`assertCapability` e remover do
  `PENDING_WIRING` — a partição obriga).
- **E4 — Mídia (M2)**: anexo referencia `tb_media` (nunca o contrário),
  evento de timeline, limite `MEDIA_MAX_PER_REPORT` (129), blur nas
  críticas (128), `expires_at` carimbado na resolução (131).
- **E5 — Retenção**: task 21 previa job SQL próprio; o mecanismo agora é o
  scheduler (90) + crypto-shredding (131). A purga de Child (25) vira mais
  uma regra do job existente; a 131 estende a régua a toda evidência.
- **E6 — Idempotência da fila offline**: a fila da decisão 28 reenvia; sem
  chave de idempotência, retry = denúncia duplicada (pendência 6).
- **E7 — Identidade**: `reporterId` = `UserAccount.id` (app plane) ou NULL
  (anônimo, rastro pelo log 23). As tasks 16-18 da spec (auth por
  provider em /auth) foram superadas pelas decisões 119-124 já
  implementadas.
- **E8 — Números de migração/arquivos**: `001_reports.sql` etc. estão
  tomados; usar a numeração corrente (030+) e módulos no padrão atual.

## 3. Desenho técnico (decisões de engenharia, não de produto)

- **Feed geográfico sem extensão espacial**: bounding box por índice
  composto (lat, lng) + refinamento haversine no SQL — simples, testável,
  suficiente para o MVP; migrar para SPATIAL index é otimização futura.
- **Raio dinâmico** (7/29): estratégia por categoria no módulo
  help-matching lendo a tabela da decisão 7; nada de raio fixo global
  (critério de sucesso 8).
- **Timeline** (19): tabela append-only `tb_report_timeline` — eventos de
  criação, edição, anexo, resolução; é o que o app renderiza.
- **Alto risco nas leituras** (40/41/60, task 24): tier lido em runtime
  (nunca gravado no Report); respostas de categoria alta sem timestamps
  por oferta e sem identidade de helper.
- **Visibilidade pós-resolução** (50, task 25): participante vê tudo;
  terceiro vê só o desfecho.
- **App**: telas novas consultam o catálogo `vgr_widgets` ANTES (133);
  fila offline com estados visíveis; HEIC→JPEG na captura (emenda M1).

## 4. Fases de execução (aguardando rodada 8; liberação fase a fase — 38)

- **R1 — núcleo do submit (API) — EXECUTADA em 2026-08-03**: emendas E1-E8
  registradas na spec; migração 030 (tb_report com XOR de taxonomia,
  client_key único, posição exata, frozen/expires prontos p/ R3 +
  tb_report_timeline append-only); VOs dos dois eixos em código (140);
  `POST /app-reports` com optionalAppAuth (promovido ao gateway);
  `report.anonymous` CABEADA (removida do PENDING_WIRING — cobre também
  logado-escolhendo-anonimato, 32); idempotência 137 com replay 200 e
  corrida ER_DUP_ENTRY resolvida; validação 47 via
  `shared/risk/category-form` (promoção E8, cache único); accountability
  23 via `shared/audit/accountability` (promoção E8). 47 suítes / 282
  testes. Doc: `api/docs/feature/reports.md`.
- **R2 — feed (API) — EXECUTADA em 2026-08-03**: `GET /app-feed` anônimo
  (critério 2); raio dinâmico por categoria×sujeito (7/29 — tabela única
  em TS compilada para o SQL, missing×animal vagueia, missing×child
  escala mais rápido, assault fixo 2 km); ST_Distance_Sphere + raio no
  SQL, relevância determinística (21); **degradação por tier (135/41)**:
  grade de posição (0.001/0.005/0.01°), distância derivada da posição
  DEGRADADA (anti-trilateração), tempo em balde (minuto/15min/hora), sem
  reporter/engajamento; promoções: `shared/risk/risk-tier` (extração que
  a task 32 sinalizava) e `shared/taxonomy`; migração 031 semeia tier
  consciente por categoria (assault=high — 'low' acidental exporia a casa
  da vítima); categoria renomeada `missing` (140c — o que sumiu é o
  sujeito). 50 suítes / 300 testes. Doc: `api/docs/feature/help-matching.md`.
- **R3 — ciclo de vida (API) — EXECUTADA em 2026-08-03**: posse por conta
  OU clientKey portador (header x-client-key, padrão 134); edit só
  aberto+não congelado com re-validação 47 (19); resolve atômico
  carimbando expires_at+90d (18/131); GetReportVisibility (50) — owner
  com ofertas mascaradas por tier (6/40/41/60), participante sem lista,
  público degradado pela MESMA grade do feed (shared/geo/degrade,
  promoção do R3); /app-help-offers (10/20/34/35 — anti-fraude,
  anônimo pleno, 409 duplicata, timeline sem identidade);
  /api/case-freeze (141/142 — congela 1 humano com motivo, descongela
  por dual-control de usuários distintos, prazo recomeça, SEM evento de
  timeline para não avisar investigado; tudo auditado); job report-purge
  no scheduler (25/131 — esqueleto estatístico fica). Migração 032.
  53 suítes / 333 testes.
- **R4 — mídia M2 (API) — EXECUTADA em 2026-08-04**: migração 033
  (`tb_report_media` — o anexo referencia tb_media, E4; seed da capacidade;
  flip dos 'available' órfãos para 'pending'); ciclo de vida da 134 ativo
  (evidência nasce `pending`, o attach CONSOME o estado numa transação
  atômica link+claim+timeline — replay da fila responde 200 `replayed`,
  segundo report leva 409); `POST /app-reports/:id/media` com posse
  (publicId portador p/ anônimo, mesma conta p/ autenticado), limite
  MEDIA_MAX_PER_REPORT (129), accountability no attach anônimo (23) e
  `report.media` cabeada no service (138 — nunca entrou no
  PENDING_WIRING; guard do catálogo agora varre TODAS as migrations);
  `GET /app-reports/:id/media/:publicId/:variant?` = único caminho de
  leitura da mídia anônima, visibilidade do report (público de tier alto
  só recebe `blur` — 128; resolvido só participante — 50; original nunca
  sai do painel — 130); órfã expira por `MEDIA_ORPHAN_TTL_HOURS` (48h,
  config — 136) no job existente; resolve carimba o MESMO relógio nas
  mídias (131) e freeze/unfreeze cobrem o caso INTEIRO com relógio
  reiniciado (141b/d); leitura do dono no /app-media aceita `pending`.
  Promoção E8: `shared/storage/media-object` (chave+decifra, 2º leitor).
  54 suítes / 356 testes. Docs: `api/docs/feature/reports.md` + `media.md`.
- **A1 — app: denunciar — EXECUTADA em 2026-08-04** (commit 1415625 do
  app): primeiro feature real do apps/mobile (era esqueleto) — bootstrap
  EasyLocalization+Modular no padrão do admin; módulo report (Clean, spec
  tasks 03-06/21 emendadas MA1-MA7 na spec mobile); dois eixos
  obrigatórios (140, XOR na entidade); formulário dinâmico do catálogo
  `category-forms` cacheado local com pré-validação offline (47);
  `OfflineQueueService` no packages/core (task 16, decisão 28 — FIFO
  persistida, retry para o flush, cadeia submit→upload→attach replay-safe
  por clientKey 137 e header x-client-key 134); fotos em background nunca
  travando a denúncia (123), escolha EXIF por foto com aviso v1 e versão
  gravada (86/130/139), reforço no fluxo anônimo; posição obrigatória
  atrás de LocationGateway (7/135); tudo Vgr* com guarda replicada (133 —
  novos VgrPhotoThumb/VgrWrap). Suítes: core 31, admin 79, mobile 37.
  Doc: `app/docs/feature/report-form.md`. Nota: HEIC→JPEG na captura é
  pré-requisito de build iOS (porta documentada), MVP Android.
- **A2 — app: feed + detalhe/timeline — EXECUTADA em 2026-08-04**: feed
  virou a home (form em /new atrás de FAB — 123); GET /app-feed anônimo
  com tudo degradado por tier (135), paginação por botão com dedupe
  (21), ordenação recency|relevance; detalhe renderiza estritamente pelo
  `access` do servidor (50) — summary só desfecho, public com posição
  "aproximada", owner com timeline e ofertas mascaradas (40/41/60);
  mídia por `VgrNetworkImage` com variante pelo tier (blur-only público
  em high — 128) e header x-client-key; `MyReportsStore` persiste
  reportId→clientKey nos DOIS caminhos de submit (134 — fecha o loop do
  A1). Suítes: core 31, admin 79, mobile 60. Doc:
  `app/docs/feature/report-feed.md`.
- **A3 — app: oferecer ajuda — EXECUTADA em 2026-08-19**: módulo
  `help_offer` próprio (Clean, spec tasks 09/10/19 emendadas MA8-MA10);
  `POST /app-help-offers` com `{reportId, helpType, anonymous}` — enum
  fechado da decisão 10, sem fila offline (oferta responde a caso vivo;
  falha de transporte = OFFLINE e o usuário tenta de novo); guarda de
  self-dealing (20) DUPLA pela posse do clientKey (134, porta
  `OwnsReport`): bloc desabilita o form com mensagem (cobre deep link
  forjado) e usecase corta antes da rede; botão "Oferecer ajuda" só em
  `access == public && status == open` (dono vê ofertas — 20; resolvido
  não aceita oferta nova — 18); aviso de inelegibilidade de recompensa
  para TODO helper anônimo (34/35, MA9 — estreitar quando o domínio
  Reward existir), nunca bloqueia o envio; 409 DUPLICATE traduzido por
  código (80/83); detalhe recarrega após oferta (timeline
  `help_offered` sem identidade). Suítes: core 31, admin 79, mobile 79.
  Doc: `app/docs/feature/help-offer.md`.
- **P1 — painel: tela mínima do congelamento — EXECUTADA em 2026-08-19**
  (commits 7337c73 da API e 7f8935b do app): migração 034 promove a
  interface `case_freeze` de kind 'R' (escolha da R3, quando só existia
  API) para 'T' — mesma linha, mesmos grants, agora visível no menu
  dinâmico; módulo `case-freeze` no apps/admin em `/case-freeze`
  (`interface_routes` + AdminSessionGuard): busca por id e UMA ação por
  vez decidida ESTRITAMENTE pelo estado do servidor (bloc re-busca após
  cada mutação — a tela nunca adivinha transição): congelar com motivo
  obrigatório (141, mínimo de 3 espelhado do DTO), solicitar
  descongelamento (passo 1) e aprovar (passo 2 — usuário DISTINTO e
  relógio reiniciado são juízo do servidor; o 422 de mesmo usuário
  renderiza verbatim); botões UPDATE desabilitados sem grant (72).
  Busca completa/moderação/estatísticas seguem como frente própria
  (142). Suítes: core 31, admin 93, mobile 79; API 54/357. Doc:
  `app/docs/feature/case-freeze.md`.

Cada fase fecha com suíte verde, feature doc e commit — padrão das
frentes anteriores.

## 5. Rascunho do aviso EXIF v1 (pendência 8 — aprovar/editar)

Texto exibido quando o denunciante toca em "manter dados probatórios da
foto" (decisão 130; chave i18n, pt-BR abaixo, en-US na tradução):

> **Manter dados técnicos da foto?**
> Esta foto carrega informações invisíveis: onde ela foi tirada (GPS),
> quando, e com qual aparelho. Mantê-las pode ajudar como prova — mas
> também **revela onde você estava**.
> Se você preferir se proteger, descarte: a foto continua valendo, sem os
> dados técnicos. Só quem tem autorização especial e auditada consegue ver
> os dados mantidos.
> [Descartar dados (recomendado)] [Manter como prova]

Variante reforçada no fluxo anônimo (um parágrafo a mais):

> Você escolheu denunciar anonimamente. Os dados técnicos desta foto podem
> revelar sua localização e contradizer esse anonimato. Mantenha apenas se
> entender esse risco.

Versionamento: `exif-warning/v1` gravado por foto (padrão da decisão 86).
