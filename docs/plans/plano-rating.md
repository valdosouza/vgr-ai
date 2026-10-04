# Plano — Rating de helpers pelo denunciante (decisão 48)

> **Rodada 13 — FECHADA em 2026-09-03** (rodada 0 e rodada 1 no mesmo
> dia). Decisões **178–189** registradas no
> [VGR-plano.md](../decisions/VGR-plano.md). Execução RT1 → RT2 → RT3,
> cada fase liberada por "pode seguir" (38). **RT1 executada em
> 2026-09-03** (api `ee029bc`); **RT2 executada em 2026-09-04**
> (app `0035867`); **RT3 executada em 2026-09-04** (api `b2388a9`,
> app `5a9c155`). **FRENTE COMPLETA.**
> Frente escolhida por Valdo em 2026-09-03 entre pânico / rating /
> direction sightings / sinalizar conteúdo.

---

## 1. Contexto

A decisão 48 criou o conceito: **o denunciante avalia o helper ao
finalizar a denúncia; o rating acumula na identidade INTERNA do helper**
(padrão da 23 — a plataforma sabe quem é, a interface não mostra), mesmo
quando o helper é anônimo pro denunciante, e "pode alimentar o peso de
confiança usado na decisão 27" (apontamentos de direção). A spec tática
desenhou `HelperRating` (raiz de agregado em Identity & Trust),
`RatingScore` inteiro 1–5 "nunca num perfil público", o caso de uso
`RateHelper` "na finalização do report", o evento `HelperRated`
`{ratingId, reportId, helperInternalId, score}` e dois cenários (004,
emendados em 2026-08-22: "nenhum código existe"): persiste na identidade
interna mesmo com helper anônimo; rejeita segunda avaliação na mesma
oferta.

**O que já existe e condiciona o desenho (evidência, 2026-09-03):**

| Peça | Estado | Consequência para o rating |
|---|---|---|
| `POST /app-reports/:id/resolve` (`reports.routes.ts:53`, `optionalAppAuth`; dono = conta OU `x-client-key`, 134) | R3 — grava `status='resolved'`, `resolved_at`, `expires_at = +90d`; timeline `resolved`; fecha chat (409), novas ofertas, edição e mídia | O gancho "ao finalizar" existe na API. **Não há motivo de encerramento nem "qual helper ajudou"** gravado em lugar nenhum |
| Tela de encerrar no mobile | **NÃO EXISTE** — `ReportRepository` só tem `submit`, `getCategoryForms`, `listNearby`, `getReport`; nenhuma chamada a `/resolve` no Flutter | A frente do rating precisa carregar o encerramento no app, ou não há "finalização" para avaliar |
| `tb_help_offer` (032): `helper_account_id INT NULL`, `anonymous CHAR(1)`, `help_type`, `UNIQUE (report, helper_account)`; **sem coluna de status** | R3 — dono não aceita/recusa oferta; nada marca oferta como cumprida | Rating é por **oferta** (spec); não existe "aceite" para condicionar |
| Helper com conta que escolheu anonimato | `help-offers.service.ts:37-48` grava **sempre** `helperAccountId` e marca `anonymous='S'` (23/32) | Tem identidade interna estável → **avaliável** sem quebrar a máscara |
| Helper **sem** conta | `helper_account_id = NULL`; único rastro é `tb_accountability_log` (`help_offer.submit`) | **Não tem identidade interna** — a 48 não tem onde acumular. Mesmo problema que a 169 (chat) fechou exigindo conta |
| Denunciante anônimo | `x-client-key` prova posse do report (134/137); `MyReportsStore` guarda as chaves no aparelho | Denunciante sem conta **pode** avaliar pelo mesmo mecanismo; accountability (23) como no `help_offer.submit` |
| Máscara da oferta (`reports.service.ts:444-452`) | `helperDisplayName` null quando anônimo OU tier high (6/40/60) | A tela de avaliação mostra a oferta como o detalhe já mostra: tipo de ajuda + rótulo; nunca mais que isso |
| Visibilidade pós-encerramento (50) | terceiros veem só o status; participantes (18) veem tudo | Avaliações são conteúdo de participante; helper vinculado continua vendo o caso — precisa de regra do que ele vê da própria avaliação |
| Reward (035/036): `tb_reward_recipient` (helpers fixados na reserva, 147), `tb_reward_resolution` (fulfilled/not_fulfilled por mediador, duplo controle 148) | R0+ | Já existe um "julgamento de cumprimento", mas é ato de **mediador**, só com dinheiro reservado. Rating é ato do **denunciante**, com ou sem recompensa — conceitos distintos, não fundir |
| Estatísticas do painel (164/165) | piso k=5 em `shared/stats/k-anonymity.ts` | Agregado por helper com poucas avaliações revela a avaliação individual → mesmo piso |
| Retenção/purge (131) | `purgeExpiredReports` zera detalhe/posição/payloads/texto do chat, mantém esqueleto | Rating é reputação, não evidência do caso: precisa de regra própria |
| Moderação (162): caso oculto | escrita fechada, leitura mantida | Avaliação dada num caso oculto conta ou não no agregado? |
| Legal Gate (76–79, 176) | capacidade nova nasce `PENDING_WIRING` (`shared/legal/capabilities.ts`); espelho em `tb_legal_capability` | Reputação é perfilamento de pessoa (LGPD) — candidata a capacidade |
| Migrações | última `044_chat_evidence.sql` | próxima **045** (a spec cita `011_helper_rating.sql` — número há muito tomado; emendar) |
| `vgr_widgets` | sem widget de estrelas/nota | `VgrRating` novo (133) |
| Fila offline (`packages/core/.../offline_queue_service.dart`) | `report_queue_tasks.dart`, `chat_queue_tasks.dart` | `rating_submit` (e `report_resolve`) com `clientKey` (137) |
| Painel: detalhe do caso lista ofertas (`report_detail_page.dart:338-355`, 160) | B1 | Lugar natural para mostrar a avaliação de cada oferta |
| Direction sightings (22/26/27) | **nenhum código** | O consumo do rating como peso fica para a frente própria; aqui só se deixa o agregado legível |

## 2. Invariantes que a frente NÃO pode tocar

- Rating acumula na identidade interna e **nunca** expõe identidade a
  quem avalia (48/23/60); a tela de avaliação não pode mostrar do helper
  mais do que a oferta já mostra (6/40/55/60).
- `RatingScore` nunca aparece em perfil público (spec 003:134); nada de
  ranking de helpers visível a usuários.
- Em tier high, nenhum sinal de engajamento em tempo real ao denunciante
  (41) — avaliação só depois de encerrar já respeita isso.
- Anti-fraude de papel (20): quem avalia é o dono do report; o dono não é
  helper do próprio report.
- Uma avaliação por oferta (spec); idempotência por `clientKey` (137).
- Erro só em inglês com `code` (80/83); enforcement no servidor (72/110);
  endpoint nasce com gate/privilégio; log sem IP/localização.
- Nenhum widget Flutter direto (133); validação via `vgr_validators`.
- Nada de contato direto ou texto livre sem passar pela mesma régua do
  chat (171) — se houver texto.

## 3. Objetivos (confirmados pelas decisões 178–189)

1. Denunciante encerra a denúncia pelo app e, no mesmo fluxo, avalia cada
   helper que ofereceu ajuda (opcional, pode pular).
2. A avaliação persiste contra a conta do helper, mesmo anônimo pro
   denunciante; helper sem conta fica fora (avisado antes de oferecer).
3. Helper enxerga a própria reputação agregada, nunca por caso.
4. Nenhum usuário vê reputação de outro no MVP; o agregado fica pronto
   para a 27.
5. Painel vê a avaliação por oferta no detalhe do caso.
6. Rating sobrevive ao purge do caso; capacidade no Legal Gate; testes;
   docs.

## 4. Fatiamento (decisão 178 — RT1 → RT2 → RT3)

| Fase | Entrega | Depende de |
|---|---|---|
| **RT1 — API** — **EXECUTADA em 2026-09-03** (api `ee029bc`; 93 suítes/944 testes; migração 045 aplicada em dev). Módulo `src/modules/ratings/` (a spec previa `identity`, que não tem router por desenho — emendada); rota de avaliar montada em `app.ts` no caminho completo com `mergeParams` antes de `/app-reports`; gate 451 depois das checagens e antes do INSERT (padrão da casa); replay = convenção do `reports.submit`; contrato em `api/docs/feature/rating.md`. **Anotado**: `parseIdParam` e `owns()`/`actorOf()` duplicados entre chat/rating/reports (candidatos a `shared/http`); `docs/feature/legal-gate.md` STATUS desatualizado | Migração 045: `tb_helper_rating` (`tb_help_offer_id` UNIQUE, `tb_report_id`, `helper_account_id NOT NULL`, `score TINYINT` CHECK 1–5, `client_key` UNIQUE, `created_at`, `deleted`) + capacidade `helper.rating` (PENDING_WIRING → cabeada). `POST /app-reports/:id/offers/:offerId/rating` (dono, caso resolvido, helper com conta, gate 451, 409 se caso aberto, 422 `RATING_NOT_ALLOWED` se helper sem conta, replay por `clientKey` devolve a mesma); `GET /app-reports/:id` visão do dono ganha `offers[].rating {score|null, ratable}`; `GET /app-ratings/me` (helper autenticado): `{count, average|null}` com piso k=5; accountability `helper_rating.submit` (23); purge preserva a linha; agregado exclui casos ocultos (187). Specs 003/004 emendadas (módulo/migração reais); `docs/feature/rating.md` | — |
| **RT2 — Mobile** — **EXECUTADA em 2026-09-04** (app `0035867`; mobile 262 testes, era 195; `vgr_widgets` +4). Sem tela nova: botão "Encerrar denúncia" (confirmação, fila offline `report_resolve`; 422 "already resolved" tratado como sucesso) e o controle `VgrRating` por oferta entram na própria `report_detail_page.dart` — funciona logo após encerrar e em qualquer revisita (181); módulo `rating` só com repositório/usecases, ligado no `AppModule`; "Minha reputação" na `account_page.dart`; aviso ao helper sem conta ganhou legenda irmã (`offer-anonymous-no-rating-notice`) | RT1 |
| **RT3 — Painel** — **EXECUTADA em 2026-09-04** (api `b2388a9`, app `5a9c155`; api 93/946 testes; admin 288, era 286). `findOffersForPanel` ganhou o mesmo LEFT JOIN em `tb_helper_rating` da RT1 (só a nota, sem `ratable`, sem identidade de quem avaliou); a tela de detalhe do caso mostra a nota no `trailing` da linha da oferta, reaproveitando o `VgrRating` da RT2 em modo leitura. Sem capacidade nova, sem migração nova, sem tela de agregado por helper. Distribuição de notas na B4 fica como visão | RT1 |

## 5. Alternativas que estavam em cima da mesa (escolhas nas decisões 179–189)

### 5.1 Encerramento no app (pergunta 2)
- (i) **Entra nesta frente (RT2)**: botão "Encerrar" no detalhe do dono,
  confirmação, depois a avaliação. Sem encerrar não há "finalização".
- (ii) Encerramento vira mini-frente própria antes do rating.
- Sub-item: encerrar pede um **desfecho** (resolvido com ajuda / resolvido
  sem ajuda / desisti) gravado em `tb_report`? (a) não, só encerra
  (escopo mínimo); (b) sim — útil para estatística (B4), mas é campo novo
  no report e decisão de produto à parte.

### 5.2 Quem pode ser avaliado (pergunta 3)
- (i) **Só helper com conta** (mesmo anônimo — a máscara cobre); helper
  sem conta não é avaliável e o app avisa antes da oferta (mesma régua da
  169). Nenhum segundo segredo portador.
- (ii) Gravar avaliação "órfã" (sem `helper_account_id`) só para
  estatística do caso — não constrói reputação de ninguém.
- (iii) Bearer secret para helper sem conta (rejeitado na 169 pelo mesmo
  motivo).

### 5.3 Quando se pode avaliar (pergunta 4)
- (i) **Só com o caso resolvido**, no fluxo de encerramento e depois, até
  o purge (90 d, 131): avaliar não é obrigatório para encerrar ("a
  denúncia nunca espera", 123) e pode ser feito mais tarde no detalhe.
- (ii) Só no ato de encerrar (janela única).
- (iii) A qualquer momento após a oferta, caso aberto inclusive — mais
  cedo, mas vira sinal de engajamento durante o caso (41) e instrumento
  de pressão.

### 5.4 Escala e conteúdo (pergunta 5)
- (i) **Nota inteira 1–5, sem texto** (spec `RatingScore`). Texto livre é
  canal de retaliação/contato e exigiria filtro (171) + leitura no painel.
- (ii) Nota 1–5 + comentário curto (máx. 280) passando pelo filtro
  anti-contato, visível **só ao painel** (evidência de abuso).
- (iii) Polegar para cima/baixo.

### 5.5 Unicidade e imutabilidade (pergunta 6)
- (i) **Uma por oferta, imutável** (append-only, como o chat 177);
  segunda tentativa → 409 `ALREADY_RATED`; replay do mesmo `clientKey`
  devolve a mesma (137).
- (ii) Uma por oferta, editável até o purge (última vale).

### 5.6 O que o helper vê (pergunta 7)
- (i) **Só o próprio agregado** (`count`, `average`), e a média só com
  `count` maior ou igual a 5 (piso k=5, 164/165) — antes disso "ainda sem
  avaliações suficientes". Nunca por caso: saber "o caso X me deu 1"
  aponta o denunciante e alimenta retaliação (6/40).
- (ii) Vê por caso (nota no detalhe do caso resolvido em que participou).
- (iii) Não vê nada — reputação é só interna (27).

### 5.7 O que os outros veem (pergunta 8)
- (i) **Nada no MVP** — spec: "nunca num perfil público". Reputação
  alimenta a 27 (futuro) e o próprio helper (5.6).
- (ii) Faixa qualitativa ("novo" / "experiente") na oferta ao denunciante,
  nunca em tier high (41).
- (iii) Média numérica na oferta.

### 5.8 Painel (pergunta 9)
- (i) **Avaliação por oferta no detalhe do caso**, sob a `reports` VIEW
  (não é identidade; o painel já vê `accountId` opaco do helper, 160).
  Agregado por helper **não** ganha tela (não há tela de conta de helper
  no painel).
- (ii) (i) + distribuição de notas nas estatísticas B4 (piso k=5).
- (iii) Nada no painel nesta frente.

### 5.9 Retenção, purge, caso oculto (pergunta 10)
- Purge: (i) **rating sobrevive** — é reputação, não evidência; a linha
  guarda só ids e nota (nada a zerar), como o esqueleto do chat; (ii)
  purga junto (reputação zeraria em 90 d, esvazia a 48).
- Congelado (141): nada muda (leitura/escrita normais).
- Caso oculto (162): (a) avaliação conta no agregado; (b) **excluída do
  agregado** enquanto oculto (JOIN em `tb_report.hidden` na leitura —
  caso oculto é suspeita de abuso, e o par denunciante/helper fraudulento
  é o vetor óbvio de inflar reputação); reaparece ao reexibir.

### 5.10 Legal Gate (pergunta 11)
- (i) **Capacidade `helper.rating`** nasce `PENDING_WIRING` e é cabeada na
  RT1 (padrão 176): reputação é perfilamento de pessoa, risco varia por
  jurisdição; bloqueada → 451 antes de gravar.
- (ii) Sem capacidade — tratada como parte de `report.*`.

### 5.11 Peso de confiança da 27 (pergunta 12)
- (i) **Fora desta frente**: RT1 só deixa `findByHelperInternalId`/agregado
  prontos; a fórmula de peso nasce na rodada de direction sightings.
- (ii) Já gravar um `trust_weight` derivado (ex.: média normalizada) na
  conta do helper — cria regra antes de haver consumidor.

## 6. Fora de escopo (visões registradas)

- Rating do denunciante pelo helper (ninguém pediu; abriria vetor de
  retaliação simétrico).
- Reputação visível a outros usuários (5.7 ii/iii) — quando houver volume.
- Comentário textual (5.4 ii) — se o painel precisar de evidência.
- Desfecho do encerramento em `tb_report` (5.1 b) — decisão de produto.
- Fórmula de peso (27) — frente de direction sightings.
- Push ao helper "você foi avaliado" (11).

## 7. Critérios de sucesso

1. Dono encerra a denúncia pelo app, com ou sem rede (fila), uma vez só.
2. Após encerrar, cada oferta de helper com conta pode receber exatamente
   uma nota 1–5 do dono; replay não duplica; helper sem conta → erro
   tipado e a tela nem oferece.
3. A tela de avaliação não mostra do helper nada além do que o detalhe já
   mostrava (teste de máscara em tier high).
4. Helper autenticado lê `{count, average}` próprio; `average` é null com
   menos de 5 avaliações; nunca vê nota por caso.
5. Nenhum endpoint do plano do app devolve nota de outro usuário.
6. Purge do caso não apaga a nota; caso oculto sai do agregado.
7. Capacidade bloqueada → 451 antes de qualquer escrita.
8. Painel mostra a nota por oferta no detalhe do caso; suítes verdes nos
   dois repos; specs 003/004 emendadas; docs de feature nos dois lados.

## 8. Decisões registradas (rodada 13 — 2026-09-03)

Valdo respondeu `1 sim | 2 i-a | 3 i | 4 i | 5 i | 6 i | 7 i | 8 i | 9 i |
10 i-b | 11 i | 12 i`. Texto integral no
[VGR-plano.md](../decisions/VGR-plano.md), seção "Rating de helpers pelo
denunciante (rodada 13)".

| Item | Decisão | Resumo |
|---|---|---|
| 1 | 178 | RT1 API → RT2 mobile → RT3 painel, "pode seguir" por fase |
| 2 | 179 | Encerramento pelo app entra na RT2; sem campo de desfecho |
| 3 | 180 | Só helper com conta é avaliável (mesmo anônimo); sem conta, aviso antes da oferta |
| 4 | 181 | Só com caso resolvido, no encerramento e depois até o purge; nunca obrigatório |
| 5 | 182 | Nota inteira 1–5, sem texto |
| 6 | 183 | Uma por oferta, imutável; 409 `ALREADY_RATED`; replay por `clientKey` |
| 7 | 184 | Helper vê só o próprio agregado; média a partir de 5; nunca por caso |
| 8 | 185 | Nenhum usuário vê reputação de outro no MVP |
| 9 | 186 | Painel: nota por oferta no detalhe do caso, sob `reports`; sem tela de agregado |
| 10 | 187 | Sobrevive ao purge; caso oculto sai do agregado enquanto oculto |
| 11 | 188 | Capacidade `helper.rating` no Legal Gate, cabeada na RT1 |
| 12 | 189 | Peso da 27 fora desta frente; só o agregado fica legível |

## 9. ⚠️ Pendências

Nenhuma. Visões deixadas para rodada futura estão no §6.
