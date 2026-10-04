# Plano — Busca, moderação e estatísticas do painel (frente 142)

> **Rodada 11 — FECHADA em 2026-09-02** (rodada 0 e rodada 1 no mesmo
> dia). Nasce da decisão 142. Decisões **158–167** registradas no
> [VGR-plano.md](../decisions/VGR-plano.md). **FRENTE COMPLETA em
> 2026-09-02**: as cinco fases (B1 → B2 → B4 → B3 → B5) executadas e
> commitadas no mesmo dia. Critérios do §9 atendidos.

---

## 1. Contexto

A frente da denúncia está completa (R1–R4 na API, A1–A3 no mobile, P1 no
painel). O painel, porém, só consegue fazer **uma** coisa com um caso:
buscar por id e congelar/descongelar (`/case-freeze`, decisões 141/142).
Um operador hoje **não consegue**:

- listar denúncias (não há endpoint de busca no plano do painel — o feed
  em `/app-help-matching` é do app, degradado por tier);
- ver o conteúdo de um caso sem conhecer o id de antemão;
- tirar do ar uma denúncia abusiva ou uma imagem imprópria (o status
  `blocked` da mídia **existe** em `tb_media` e o job/leitura já o
  respeitam, mas **nenhum endpoint o escreve**; `tb_report.status` só
  admite `open|resolved`, com CHECK);
- medir nada (nenhuma agregação existe).

**O que já existe e serve de semente (evidência, 2026-09-02):**

| Peça | Onde | Estado |
|---|---|---|
| Tela P1 do congelamento | `apps/admin/modules/case-freeze`, `/api/case-freeze` | busca por id, freeze 1 humano, unfreeze dual-control; interface `case_freeze` kind 'T' em "Operations" |
| Leitura auditada de mídia no painel | `/api/media/:publicId/:variant`, guards `media_evidence` (VIEW) e `media_original` (VIEW, **sem bootstrap**) | cada leitura grava `tb_admin_audit` (116/130); `blocked` continua legível no painel |
| `tb_report` | migração 030/032 | `category`/`free_tag`/`subject`, `detail_fields`, `lat`/`lng` exatos, `anonymous`, `reporter_account_id`, `status open\|resolved`, `frozen`, `expires_at`, `purged`; índices em geo, created_at, reporter |
| Degradação por tier | `shared/geo/degrade.ts` | grade determinística por RiskTier (135) — hoje só no plano do app |
| Auditoria administrativa | `tb_admin_audit` (116) | append-only; **sem endpoint de leitura** — "tela própria é trabalho futuro" |
| Accountability log de anônimos | `shared/audit/accountability.ts` (23/44/45) | envelope-encrypted; sem leitura; o único caminho é o dual-control da 45 |
| Menu dinâmico + `can()` | `GET /api/core/menus`, `SessionAccess` (71/72) | registrar tela = 1 migração de interface + 1 rota + 1 entrada no `interface_routes` |
| Padrão de módulo no admin | `reward-mediation` (2026-08-21), `legal-policy` | módulo próprio, bloc re-busca após mutação, botões por grant |

## 2. Invariantes que a frente NÃO pode tocar

Estes já são decisão; entram aqui só para o desenho não os violar:

- **Posição exata nunca sai da API "a não ser para participantes e para
  autoridade via fluxos auditados"** (135). O painel não é participante.
- **Identidade de anônimo nunca sai fora do dual-control da 45** (23/44/
  45/60). `reporter_account_id` de denúncia anônima e o accountability
  log são invisíveis ao painel; esta frente **não** constrói o reveal.
- **Painel = configuração/governança e operação**, não cria denúncia (56).
- **Toda mutação do painel é auditada** (116); leitura de evidência
  também (130).
- **Enforcement por endpoint** (72); tela só desabilita botão.
- **Congelar/descongelar continua sendo o que a 141 diz** — esta frente
  pode *embutir* a ação no detalhe do caso, não redesenhá-la.
- **Retenção** (25/131): ocultar/moderar não é apagar; o relógio de
  expiração e o purge continuam iguais.
- **Nenhum widget Flutter direto** (133), validação de formato via
  `vgr_validators` (153–157).

## 3. Objetivos (confirmados pelas decisões 158–167)

1. Operador com grant encontra um caso sem saber o id: por período,
   categoria/sujeito, status, tier, congelado, com mídia, região
   aproximada.
2. Operador vê o caso completo **no nível que seu grant permite**, com
   leitura auditada; congela/descongela dali mesmo (reaproveitando
   `/case-freeze`).
3. Operador modera: tira imagem do ar, tira denúncia do ar, reverte — com
   motivo, auditado, sem destruir dado.
4. Existe uma fila do que precisa de olhos humanos, alimentada por sinal
   objetivo.
5. Existe leitura agregada (estatísticas) que não reidentifica ninguém.
6. Cada peça nasce com interface/privilégio próprio no catálogo, i18n e
   testes, no padrão das frentes anteriores.

## 4. Fatiamento (decisão 158 — ordem B1 → B2 → B4 → B3 → B5)

| Fase | Entrega | Depende de |
|---|---|---|
| **B1 — Busca + detalhe** — **EXECUTADA em 2026-09-02** (api `1623c90`, app `9f86945`) | `GET /api/reports` (lista paginada com filtros, posição degradada, sem auditoria), `GET /api/reports/:id` (detalhe auditado, anônimo nunca identificado, esqueleto se purgado), `GET /api/reports/:id/position` (grant empilhado `report_exact_position`, auditado, no-store); migração 038 (`reports` T, `report_exact_position` R sem bootstrap); módulo `reports` no admin (`/reports`, `/reports/:id`) com bloco de congelamento embutido, "revelar posição exata" só com o grant; `vgr_validators` ganhou `minLength(n)` e `isoDate`. Suítes: API 64/478, admin 166, mobile 140. Docs: `api/docs/feature/report-moderation.md`, `app/docs/feature/report-moderation.md`. **Pendência anotada**: painel lista a mídia como metadados (publicId/mime/status) — não há widget de imagem autenticado no painel web ainda; entra quando a B2 precisar ver a imagem para bloquear | — |
| **B2 — Moderação** — **EXECUTADA em 2026-09-02** (api `c9e74b8`, app `45eb123`) | Migração 039 (`hidden*` em tb_report, `blocked*` em tb_media); catálogo fixo em `shared/moderation/moderation-reason.ts` (nota obrigatória em `other`); `POST /api/reports/:id/hide|unhide` e `POST /api/media/:publicId/block|unblock` sob `reports` UPDATE, cada ato auditado, 409 `DUPLICATE` em hide repetido; oculto sai do feed e de toda leitura de terceiro, dono/participante veem `hidden: true` sem motivo; mídia bloqueada some do plano do app e continua legível no painel; retenção/freeze/timeline intocados. Admin: seção Moderação no detalhe (form de motivo reutilizável, `maxLength(500)` novo no `vgr_validators`), block/unblock por mídia, filtro e marca `hidden` na lista. Mobile: aviso sem motivo para o dono. Suítes: API 72/563, admin 181, mobile 144, validators 42 | B1 |
| **B3 — Fila** — **EXECUTADA em 2026-09-02** (api `cc2a0b3`, app `9952c63`) | Migração 041 (`reviewed_at`/`reviewed_by`); `GET /api/reports/queue` (abertos, não revisados, não ocultos, não purgados; ordem tier alto → médio → baixo, com mídia primeiro, mais antigo primeiro; comentário no ORDER BY marca onde o futuro sinal "sinalizar" entra acima do tier; não auditado); `POST /api/reports/:id/reviewed` (UPDATE em `reports`, auditado, 409 na 2ª marcação); filtro `reviewed` na busca; `reviewedAt/By` no detalhe. Admin: `/reports/queue` com prioridade, mídia, idade, "marcar revisado" por linha e no detalhe, filtro e marca na lista, link da lista para a fila. Suítes: API 79/643, admin 232 | B1 |
| **B4 — Estatísticas** — **EXECUTADA em 2026-09-02** (api `c5649d1`, app `cd6c376`) | Migração 040 (`report_stats` T, VIEW, bootstrap de-facto admins); `GET /api/reports/stats?from&to&granularity` (30 dias por padrão, máx. 366; não auditado): totais + por período (dia/semana ISO/mês), categoria com tier, sujeito, status, tier e motivos de moderação; piso k=5 em `shared/stats/k-anonymity.ts` aplicado DEPOIS de somar (`"<5"`); sem geo. Admin: módulo `report-stats` (`/report-stats`) com filtro validado por `isoDate`, tiles de totais, uma seção por agrupamento, legenda do piso, estado vazio. Suítes: API 76/604, admin 205 | B1 |
| **B5 — Trilha de auditoria** — **EXECUTADA em 2026-09-02** (api `8cb76c5`, app `30b3195`) | Migração 042 (`admin_audit` T, VIEW, grupo Administration, bootstrap de-facto admins; índices por created_at e action); módulo `admin-audit` na API: `GET /api/admin-audit` (paginado, filtros ator/ação/entidade/id/período, sem `ip`), `/facets`, `/:id` (com `ip`); leitura NÃO auditada, tabela segue append-only (spec prova que só há SELECT); `queryDate` promovido a `shared/http/query-date`, `AUDIT_ACTIONS` em `shared/audit/audit-action`. Admin: módulo `admin-audit` (`/admin-audit`, `/:id`) com filtros das facetas, datas validadas, detalhe com resumo em árvore e IP sob legenda de dado pessoal. Suítes: API 84/698, admin 271 | — |

Cada fase fecha com suíte verde, feature doc e commit, com liberação
"pode seguir" de Valdo por fase (38).

## 5. Alternativas que estavam em cima da mesa (escolhas nas decisões 159–167)

### 5.1 O que o painel vê do caso (pergunta 2)
- (i) **Degradado por padrão, exato por grant próprio e auditado**:
  o detalhe do painel serve a posição pela mesma grade do feed (135), e
  a posição exata só sai com a interface kind 'R' `report_exact_position`
  (VIEW, **sem bootstrap** — mesmo padrão do `media_original`), gravando
  `tb_admin_audit` a cada leitura.
- (ii) Painel vê tudo com o VIEW da tela: mais simples, mas contradiz o
  espírito da 135 ("autoridade via fluxos auditados") e concentra em um
  grant genérico o dado que em violência doméstica é a casa da vítima.

### 5.2 Identidade em denúncia NÃO anônima (pergunta 3)
O denunciante que escolheu identificar-se aceitou ser visto **por outros
usuários** (32). Isso não decide se o painel exibe a conta. Opções:
(i) painel mostra só `accountId` opaco + displayName, nunca e-mail, sob o
VIEW da tela; (ii) nada de identidade no painel fora do dual-control 45,
tratando identificado e anônimo igual; (iii) identidade completa.

### 5.3 Moderação — atos e controle (pergunta 5)
- Atos candidatos: **bloquear mídia** (`available → blocked`, reversível),
  **ocultar denúncia** (some do feed/público/detalhe de terceiros; dono e
  participantes continuam vendo; retenção inalterada), **reverter** ambos.
- Controle: (i) 1 humano com motivo + auditoria para ocultar/bloquear e
  também para reverter (nada aqui destrói prova, ao contrário do
  descongelar); (ii) reverter com dual-control.
- Modelagem: coluna própria `hidden CHAR(1)` + `hidden_reason` +
  `hidden_at` em `tb_report` (não mexe no CHECK de `status`, que é ciclo
  de vida do caso e não moderação) — ou novo valor de `status`.

### 5.4 Motivo de moderação (pergunta 6)
(i) catálogo fixo em código (`spam`, `abuse`, `illegal_content`,
`duplicate`, `other`) + texto livre obrigatório em `other`; (ii) só texto
livre (como o freeze); (iii) catálogo administrável (tela) — fora do
MVP, mesma trajetória do risk-config.

### 5.5 Fila de moderação — de onde vem o sinal (pergunta 4)
Hoje **não existe "sinalizar conteúdo" no app**. Opções: (i) fila
proativa = casos abertos ainda não revisados, priorizando tier alto e
com mídia, com marca `reviewed_at` por operador; (ii) construir o
"sinalizar" no app (capacidade nova, Legal Gate, frente mobile própria) e
a fila consome esse sinal; (iii) sem fila nesta frente — a lista com
filtros e ordenação já cobre.

### 5.6 Estatísticas — o quê (pergunta 7)
Contadores agregados por período × categoria × sujeito × status × tier,
mais congelados/ocultos/expirados/purgados. Duas questões: mapa de calor
entra (só na grade `high`, nunca ponto exato)? Piso de agregação (k
mínimo por célula, ex. contagem < 5 vira "<5") para não reidentificar
por combinação rara?

### 5.7 Interfaces/privilégios (pergunta 8)
Proposta: `reports` (T, "Operations": VIEW = buscar/ver, UPDATE = moderar),
`report_exact_position` (R, VIEW, sem bootstrap), `report_stats` (T,
VIEW). `case_freeze` continua próprio; o detalhe mostra o bloco de
congelamento habilitado pelo grant de `case_freeze`, chamando os
endpoints já existentes. `media_evidence` continua guardando a imagem.

### 5.8 Leitura auditada do caso (pergunta 9)
Ver uma foto grava auditoria (130). Ver o detalhe de um caso — com
texto livre, campos de detalhe, timeline — é evidência da mesma
natureza. Opções: (i) audita leitura do detalhe (não da lista); (ii) só
audita quando a posição exata é aberta; (iii) não audita leituras.
Correlato: a tela de leitura de `tb_admin_audit` (B5) entra nesta frente
ou fica para depois?

### 5.9 O que o denunciante vê quando ocultado (pergunta 10)
(i) nada muda para o dono/participantes além de uma marca `hidden` no
detalhe (sem motivo — motivo é da auditoria), sem evento de timeline;
(ii) evento de timeline `hidden` visível ao dono; (iii) silêncio total
(dono não sabe). O freeze escolheu "sem timeline" para não avisar
investigado; aqui o argumento é outro (abuso, não investigação).

## 6. Decisões registradas

Texto integral no [VGR-plano.md](../decisions/VGR-plano.md), seção
"Busca, moderação e estatísticas do painel (rodada 11)".

- **158** — cinco fases, ordem B1 → B2 → B4 → B3 → B5.
- **159** — posição degradada por padrão; exata só por
  `report_exact_position` (R, sem bootstrap), leitura auditada.
- **160** — denúncia não anônima: id opaco + displayName, nunca e-mail;
  anônima: nada.
- **161** — fila proativa (tier alto + mídia, `reviewed_at/by`);
  "sinalizar" no app fica como frente mobile futura.
- **162** — moderação = bloquear mídia, ocultar denúncia, reverter; 1
  humano + motivo + auditoria; coluna `hidden*` própria; retenção
  intacta.
- **163** — motivo: catálogo fixo (`spam`, `abuse`, `illegal_content`,
  `duplicate`, `personal_data`, `other` + nota).
- **164** — estatísticas agregadas com piso k = 5; sem mapa de calor.
- **165** — interfaces `reports` (T), `report_exact_position` (R),
  `report_stats` (T), `admin_audit` (T); `case_freeze`/`media_evidence`
  intactos.
- **166** — leitura do detalhe auditada; da lista não; B5 entra.
- **167** — dono vê marca `hidden`, sem motivo, sem timeline.

## 7. Fora de escopo (já claro sem pergunta)

- Reveal de identidade de anônimo / decriptação do accountability log —
  é o fluxo da 45, frente própria.
- "Sinalizar conteúdo" pelo usuário no app — frente mobile futura
  (decisão 161); quando existir, entra na mesma fila acima do tier.
- Mapa de calor das estatísticas — reabre com volume real (164).
- Catálogo administrável de motivos de moderação.
- Despacho automático a autoridades (53), moderação automática por IA.
- Exportação de caso para autoridade (ofício/PDF) — registrar como visão.

## 8. Pendências (rodada 11 — busca/moderação do painel)

**Nenhuma.** Itens 1–10 resolvidos em 2026-09-02 pelas decisões 158–167.

## 9. Critérios de sucesso

1. Operador sem grant não lista, não vê, não modera (72) — teste por rota.
2. Nenhuma resposta do plano do painel contém `lat`/`lng` exatos sem o
   grant de `report_exact_position`, e cada leitura exata grava auditoria.
3. Nenhuma resposta do painel contém `reporter_account_id` de denúncia
   anônima nem qualquer campo do accountability log.
4. Ocultar/bloquear/reverter gravam `tb_admin_audit` com motivo; o feed e
   o detalhe público do app deixam de servir o caso/mídia ocultados;
   dono/participantes continuam vendo; purge e retenção inalterados.
5. Estatísticas nunca devolvem célula com contagem abaixo do piso.
6. Guard 133 verde; suítes da API e dos dois apps verdes; feature docs
   `api/docs/feature/report-moderation.md` e
   `app/docs/feature/report-moderation.md`; `VGR-RESUMO.md` §4 atualizado.
