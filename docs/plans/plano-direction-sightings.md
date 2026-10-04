# Plano — Apontamentos de direção / Direction Sighting (decisões 22, 26, 27)

> **Rodada 15 — FECHADA em 2026-09-04** (rodada 0 e rodada 1 no mesmo
> dia). Decisões **200–207** registradas no
> [VGR-plano.md](../decisions/VGR-plano.md). Execução DS1 → DS2 → DS3
> (vazia, dado 201), cada fase liberada por "pode seguir" (38). **DS1
> executada em 2026-09-04** (api `ed242db`); **DS2 executada em
> 2026-09-04** (app `b6a15a7`). **FRENTE COMPLETA** — DS3 vazia por
> decisão (201).
> Frente escolhida por Valdo em 2026-09-04, entre as duas que restavam
> (direction sightings, sinalizar conteúdo).

---

## 1. Contexto

A decisão 22 já fixou que o apontamento de direção processa **de forma
síncrona** (agilidade da informação, não lote). A 26 fixou que a
reconciliação é um **modelo estatístico ponderado** — estimativa inicial
50/50 entre as duas direções inicialmente reportadas (ex.: norte/sul),
deslocada por apontamentos adicionais, nunca voto majoritário simples. A
27 fixou que **apontamento de helper anônimo pesa menos que o de helper
identificado** (mitigação anti-fraude, não solução completa). A 28 (já
fechada) já exige que apontamentos, como denúncias, passem pela fila
offline.

O conceito original (texto de visão do dono do produto, não numerado):
"roubo de veículo → apontamento coletivo de direção pela comunidade
(raio calculado por tempo × velocidade média); **cuidado de design**:
agregar o maior número de apontamentos antes de expor a direção, para
evitar que o ladrão faça engenharia reversa e descubra que está sendo
rastreado." Essa cautela nunca virou decisão numerada — esta rodada
formaliza isso. A decisão 11 (já fechada) deixou de fora só a parte mais
avançada — previsão de trajetória + notificação push proativa — não o
mecanismo básico de apontar/reconciliar, que já está no MVP desde a 22.

A spec tática (`003-api-tactical-design.md`) desenha o agregado inteiro
(`DirectionEstimate`, `DirectionSighting`, `SightingWeight`, enum
`Direction` de 8 pontos cardeais N/S/E/W/NE/NW/SE/SW,
`LogDirectionSighting`, `ReconcileDirectionEstimate`, módulo
`src/modules/direction-sightings/`) mas **nenhuma linha de código
existe** — confirmado por busca ampla nos dois repositórios (`direction`,
`sighting`, `compass`): zero tabela, zero módulo, zero UI.

A decisão 189 (rodada do rating) deixou uma promessa em aberto: *"o peso
de confiança da 27 fica fora da RT1; a fórmula nasce na rodada de
direction sightings, quando houver consumidor."* Essa rodada é esse
consumidor — o §5.7 abaixo decide se essa ligação entra agora.

**O que já existe e condiciona o desenho (evidência, 2026-09-04):**

| Peça | Estado | Consequência para a frente |
|---|---|---|
| Rota da spec (`POST /api/direction-sightings`) | **Mesmo bug de plano já corrigido no pânico**: a spec foi escrita antes da divisão de dois planos (119); `/api` hoje exige JWT `aud: admin` globalmente (`app.ts`, `authMiddleware`). Um apontamento é ação de usuário do app — não é decisão de negócio, é correção a aplicar direto: rota nasce em `/app-direction-sightings` (ou sob `/app-reports/:id/...`), nunca `/api` | Correção aplicada na construção, sem pergunta |
| `RiskTierConfig` (`shared/risk/risk-tier.ts` + `modules/risk-config/`) | Padrão "admin-editável, cache com TTL, nunca hardcoded" — uma linha por categoria, default em código se a linha não existir, invalidação de cache na escrita | Candidato a modelo para "quais categorias permitem apontamento" |
| `dynamic-radius.ts` (Help Matching) | Padrão OPOSTO — `STRATEGY_BY_CATEGORY` é tabela fixa no código, sem banco, sem admin | Outro candidato válido, mais simples, mesmo domínio de "comportamento por categoria de objeto em movimento" |
| Categoria (`shared/taxonomy/taxonomy.ts`) | Enum real: `assault, environmental, robbery, homicide, illegal_commerce, missing, fugitive, kidnapping, suspicious, trafficking, traffic, vandalism`. `assault` (violência doméstica) já é o exemplo "fica parado" (comentário do próprio `dynamic-radius.ts`); `robbery`/`fugitive`/`kidnapping`/`missing` são as candidatas naturais a "sujeito em fuga" | Base real para decidir elegibilidade por categoria |
| `tb_help_offer` | **Sem `client_key`/idempotência nenhuma** para oferta anônima — um insert simples, sem proteção contra replay | Contraste com reports/chat/rating/pânico (todos com `client_key` único); apontamento é agregado mais leve, mas a 28 (fila offline) exige alguma idempotência |
| Legal Gate (`shared/legal/capabilities.ts`) | `LOCATION_TRACKING: 'location.tracking'` **já existe**, em `PENDING_WIRING`, com comentário citando literalmente **"decisions 7, 22, 26"** — a capacidade já nasceu pensada pra esta frente, nunca cabeada | Reaproveitar, não criar nova |
| App mobile | Nada — `category` já chega na visão do detalhe (`ReportViewEntity.category`), ponto de anexação natural entre a posição e as ofertas | Frente inteira do lado mobile é greenfield |
| `packages/vgr_widgets` | Sem widget de "sinal agregado"/bússola; `VgrRating` é o precedente estrutural mais próximo (leitura/escrita dual por `onChanged` nullable), mas é estrelas 1–5, não direcional | `VgrCompass` (ou nome equivalente) nasce nesta frente |
| Migrações | Última: `046_panic_alert.sql` | Próxima: **047** |

## 2. Invariantes que a frente NÃO pode tocar

- Processamento síncrono (22): a resposta do apontamento já devolve a
  estimativa reconciliada, sem fila de processamento em lote.
- Reconciliação é modelo ponderado, nunca voto majoritário simples (26);
  prior 50/50 entre as duas direções inicialmente reportadas.
- Apontamento de anônimo pesa menos que o de identificado (27) — mitigação,
  não solução completa; nunca bloqueia o apontamento em si.
- Fila offline obrigatória (28) — apontamento sobrevive a estar offline
  no momento do toque, mesmo padrão de denúncia/chat/pânico.
- Posição exata nunca sai da API (135) — a direção é um sinal categórico
  (um de 8 pontos), nunca latitude/longitude.
- Responsabilização de anônimos (23): apontamento anônimo deixa trilha
  interna, nunca bloqueia o fluxo.
- Anti-fraude de papel (20): mesmo espírito aplicado aqui — quem denuncia
  não deveria poder manipular a própria estimativa de direção do próprio
  caso.
- Erro só em inglês com `code` (80/83); enforcement no servidor (72/110);
  endpoint nasce com gate/privilégio; log sem IP/localização exata.
- Nenhum widget Flutter direto (133); nenhum SDK externo fora de `shared/`
  (143).

## 3. Objetivos (confirmados pelas decisões 200–207)

1. Um usuário próximo de uma denúncia elegível registra rapidamente qual
   direção viu o sujeito/veículo/animal seguir, sem fricção.
2. Depois de apontamentos suficientes, quem vê a denúncia enxerga a
   direção mais provável — nunca antes disso, para não alertar quem está
   sendo rastreado.
3. Apontamento de quem se identificou pesa mais que o de quem não se
   identificou, sem excluir ninguém.
4. Nenhuma posição exata, nenhum apontamento individual exposto — só o
   agregado, categórico.
5. Capacidade do Legal Gate cabeada; testes; docs; specs emendadas.

## 4. Fatiamento (decisão 207 — DS1 → DS2 → DS3 vazia)

| Fase | Entrega provável | Depende de |
|---|---|---|
| **DS1 — API** — **EXECUTADA em 2026-09-04** (api `ed242db`; 101 suítes/1064 testes, era 97/1001; migração 047 aplicada em dev). Rota flat `POST /app-direction-sightings`; algoritmo promovido a `shared/direction-sighting/` (3 consumidores); `tb_direction_estimate` materializa o peso O(1); facet batched no report E no feed; `location.tracking` já estava semeada (migração 022), só cabeada | Migração 047 (`tb_direction_sighting`, `tb_direction_estimate`; config de elegibilidade por categoria SE o item 2 escolher o padrão RiskTierConfig); capacidade `location.tracking` cabeada; `POST /app-direction-sightings` (loga + reconcilia + devolve a estimativa, síncrono); `GET` da estimativa embutido na visão do report (mesmo padrão do facet `rating`/`chat`) | — |
| **DS2 — Mobile** — **EXECUTADA em 2026-09-04** (app `b6a15a7`; mobile 391 testes, era 344; `vgr_widgets` +4; `core` +2, admin sem alteração). `Direction` promovido a `packages/core` (precedente `RiskTier`); `VgrCompass` novo, deliberadamente sem depender de `core` (strings simples); estimativa somente leitura no detalhe e no item do feed; picker só para não-dono, categoria elegível, caso aberto, aparelho ainda não apontou (registro local, não é fronteira de segurança); fila offline igual rating/pânico | DS1 |
| **DS3 — Painel** | **Vazia** (decisão 201 escolheu o padrão fixo no código, sem admin) — mesmo desfecho do pânico | — |

## 5. Alternativas que estavam em cima da mesa (escolhas nas decisões 200–207)

### 5.1 Quem pode apontar uma direção (pergunta 1)
- (i) **Qualquer pessoa que veja a denúncia aberta**, anônima ou
  identificada (mesmo padrão de quem pode oferecer ajuda, 32/35) — só o
  próprio denunciante fica de fora (mesma razão anti-fraude da 20:
  poderia manipular a estimativa do próprio caso).
- (ii) Só quem já ofereceu ajuda (HelpOffer) na denúncia — mais
  restritivo, aproxima "apontar direção" de "ser helper".
- (iii) Só usuários com conta (identificados) — descarta o cuidado
  original "coletivo pela comunidade" e o peso da 27 perderia sentido
  (não haveria apontamento anônimo pra pesar menos).

### 5.2 Elegibilidade por categoria (pergunta 2)
- (i) **Configurável pelo admin**, mesmo padrão do `RiskTierConfig`
  (linha por categoria, cache com TTL, default seguro se não configurada)
  — mais flexível, mais trabalho, abre a DS3.
- (ii) **Fixo no código**, mesmo padrão do `dynamic-radius.ts`
  (`STRATEGY_BY_CATEGORY`-like) — mais simples, sem admin, sem DS3;
  ajustar a lista exige deploy.

### 5.3 Piso mínimo antes de expor a estimativa (pergunta 3)
- (i) **5 apontamentos** (mesmo número já usado no piso de k-anonimato
  das estatísticas do painel, 164/165 — consistência, não o mesmo motivo:
  ali é anonimato estatístico, aqui é anti-contravigilância), valor
  configurável por ambiente (mesmo padrão dos limites do chat, 177).
- (ii) Piso diferente — Valdo escolhe o número.
- (iii) Sem piso — a estimativa aparece desde o primeiro apontamento
  (contraria o "cuidado de design" original).

### 5.4 O que é exposto (pergunta 4)
- (i) **Só a direção mais provável** (categórica: "provavelmente norte"),
  nunca a distribuição de probabilidade completa — menor informação
  possível, mesmo princípio de todo o resto do projeto (mascarar chat,
  degradar posição, arredondar distância do pânico).
- (ii) A distribuição inteira (ex. "60% norte, 25% nordeste, 15% outros")
  — mais informativo, mais superfície pra inferência.

### 5.5 A quem é exposto (pergunta 5)
- (i) **Todo mundo que vê a denúncia aberta**, incluindo o feed público
  (mesmo alcance de "coletivo pela comunidade" do texto original) — uma
  vez passado o piso da pergunta 3.
- (ii) Só participantes (dono + quem ofereceu ajuda) — mais restrito,
  perde alcance de "mais gente ajuda a rastrear".

### 5.6 Peso exato do apontamento (pergunta 6)
- (i) **Valores fixos em código com override por variável de ambiente**
  (ex. `SIGHTING_WEIGHT_ANONYMOUS=0.5`, `SIGHTING_WEIGHT_IDENTIFIED=1.0`)
  — mesmo tratamento que os limites do chat (177) ganharam: número
  operacional, não decisão travada.
- (ii) Valdo fixa os números exatos agora, como decisão.

### 5.7 Peso de confiança da reputação (pergunta 7 — fecha a promessa da 189)
- (i) **Não entra nesta rodada** — a fórmula fica só identificado vs.
  anônimo (27), como já decidido; incorporar a média de avaliações
  (rating, RT1-RT3) fica registrado como refinamento futuro, quando
  houver evidência de que o peso simples não basta. Mesmo raciocínio que
  a 189 já usava: "regra sem consumidor validado é regra sem teste."
- (ii) **Entra agora** — o peso de um apontamento identificado escala
  pela média de avaliações da conta (`GET /app-ratings/me`-style,
  já entregue); helper sem avaliações suficientes (piso k=5, 184) usa o
  peso neutro da 27. Mais fiel à intenção original da 27/189, mais
  acoplamento entre frentes (o serviço de apontamento passa a ler o
  agregado de `ratings`).

### 5.8 Fatiamento (pergunta 8)
- (i) **DS1 API → DS2 mobile → DS3 painel (só se a pergunta 2 escolher
  i)**, cada fase por "pode seguir" (38), API sempre sem pendência antes
  da próxima fase ([[metodo-fase-api-sem-pendencia]]).
- (ii) Fatiamento diferente, a propor.

## 6. Fora de escopo (visões registradas, independente das respostas acima)

- Previsão de trajetória + notificação push proativa (decisão 11, já
  fechada como fora do MVP — não repropor).
- Elegibilidade de apontamento pra recompensa (nada na visão original
  sugere isso; apontar direção não é um dos tipos de ajuda da decisão 10).
- Modelo de velocidade por categoria (pessoa a pé/veículo/animal) — parte
  da previsão de trajetória, já fora (11).
- Revogar/editar um apontamento já registrado — nada na spec sugere que
  isso exista; apontamento é sinal de mão única, append-only.

## 7. Critérios de sucesso

1. Um apontamento síncrono devolve a estimativa reconciliada na mesma
   resposta, nunca em lote.
2. Antes do piso mínimo, nenhum viewer vê direção nenhuma — só depois.
3. Um apontamento anônimo pesa menos que um identificado na reconciliação,
   sem nunca ser recusado por isso.
4. Nenhum apontamento individual, nenhuma posição exata, é exposto a
   ninguém — só o agregado categórico.
5. O denunciante do próprio caso não consegue apontar direção nele.
6. Capacidade bloqueada → 451 antes de qualquer escrita.
7. Suítes verdes nos dois repositórios; specs 003/004 emendadas; docs de
   feature nos dois lados (ou só na API, se DS2/DS3 vierem depois).

## 8. Decisões registradas (rodada 15 — 2026-09-04)

Valdo respondeu `1 i | 2 i | 3 i | 4 i | 5 i | 6 i | 7 i | 8 i` — todas
na opção recomendada. Texto integral no
[VGR-plano.md](../decisions/VGR-plano.md), seção "Apontamentos de
direção / Direction Sighting (rodada 15)".

| Item | Decisão | Resumo |
|---|---|---|
| 1 | 200 | Qualquer visualizador aponta, anônimo ou identificado; só o denunciante fica de fora |
| 2 | 201 | Elegibilidade por categoria fixa no código, padrão do raio dinâmico |
| 3 | 202 | Piso de 5 apontamentos antes de expor, configurável por env |
| 4 | 203 | Só a direção mais provável, nunca a distribuição completa |
| 5 | 204 | Exposta a todo mundo que vê a denúncia, incluindo feed público |
| 6 | 205 | Peso fixo no código com ajuste por env |
| 7 | 206 | Peso de reputação NÃO entra nesta rodada (fecha a promessa da 189) |
| 8 | 207 | Fatiamento DS1 → DS2 → DS3 (vazia) |

Confirmadas sem mudança: direção como enum de 8 pontos cardeais; Legal
Gate reaproveita `location.tracking` (já declarada, cabeada nesta
frente).

## 9. ⚠️ Pendências

Nenhuma. Visões deixadas para rodada futura estão no §6.
