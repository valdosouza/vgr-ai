# Plano — Oferta de ajuda com vários tipos (rodada 16 — revisa a leitura singular da decisão 10)

> **Rodada 16 — FECHADA em 2026-09-11** (rodada 0 e rodada 1 no mesmo
> dia). Decisões **208–214** registradas no
> [VGR-plano.md](../decisions/VGR-plano.md). Pedido de Valdo em
> 2026-09-10, no primeiro teste com dois atores reais (Motorola +
> Chrome). Execução HT1 → HT2 → HT3, cada fase por "pode seguir" (38);
> API sem pendência antes de mobile/painel (método 2026-09-04).
> **HT1 executada em 2026-09-11** (api: migração 049 aplicada em dev, 1116
> testes verdes; commit no log do git). **HT2 executada em 2026-09-19**
> (app: bloc com `Set<HelpType>`, checkboxes múltiplos de verdade, botão
> desabilitado com zero marcados, "Alterar tipos de ajuda" no detalhe do
> participante em denúncia aberta, tipos separados por " · "; 428 testes
> verdes). **Adendo HT1 na mesma data**: a visão de participante de
> `GET /app-reports/:id` passou a devolver `myOffer { helpOfferId,
> helpTypes }` — sem isso o app não sabia qual oferta a 211 edita nem o
> que já estava marcado (1117 testes verdes na API). **HT3 executada em
> 2026-09-19** (painel: entidade e linha da oferta com `helpTypes`; 289
> testes verdes). **FRENTE COMPLETA.** Hashes: ver log do git de `api/` e
> `app/`.

---

## 1. Contexto

A decisão 10 lista os tipos de ajuda que "o helper escolhe ao se
candidatar": presença física, repassar informação a autoridades, apoio
remoto/orientação, divulgar/compartilhar, contribuição financeira. Ela
não diz "um só", mas tudo que veio depois leu no singular:

| Onde | Como está hoje |
|---|---|
| Spec tática 003 | `submitHelpOffer(reportId, helperId, type: HelpType)`; evento `HelpOfferSubmitted { helpOfferId, reportId, helperId, helpType }`; task 06 "HelpOffer aggregate with HelpType selection" |
| Cenários 004 | "persist and retrieve a HelpOffer with its chosen HelpType intact"; `POST /api/help-offers { reportId, helpType }` |
| Migração 032 | `tb_help_offer.help_type VARCHAR(30) NOT NULL` + `CHECK chk_offer_type`; `UNIQUE (tb_report_id, helper_account_id)` = **uma oferta identificada por helper por denúncia** |
| API | `help-offers.dto.ts` `helpType: z.enum(HELP_TYPES)`; `help-offers.service.ts` grava um tipo e emite `help_offered { helpType }` na linha do tempo; `reports.repository.ts` lê `o.help_type` nas visões dono/participante e no detalhe do painel (`reports-admin.service.ts`) |
| Mobile | `help_offer_form_page.dart` desenha **checkboxes** (`VgrCheckboxTile`) mas o bloc guarda um único `selected` — visualmente múltiplo, comportamento de rádio (a confusão que Valdo viu) |
| Painel | `report_detail_page.dart` mostra `reports.detail.helpType.<tipo>` por oferta |
| Dependentes da oferta | `tb_reward_recipient.tb_help_offer_id` (035), `tb_chat_thread.help_offer_id` (043), `tb_helper_rating.tb_help_offer_id` (045) — todos apontam para **a oferta**, nunca para o tipo |

O que NÃO muda com esta rodada: a oferta continua sendo o vínculo
helper ↔ denúncia (uma por helper identificado por denúncia, `uq_offer_helper`);
chat, rating e recompensa continuam pendurados na oferta.

## 2. Objetivos

1. O helper marca **um ou mais** tipos de ajuda na mesma oferta.
2. Dono, participante e painel veem **todos** os tipos da oferta.
3. Spec 003/004 emendadas antes do código (invariante 5 — "Amended").
4. Nada muda em chat, rating, recompensa e no limite de uma oferta por helper.

## 3. Proposta fechada (decisões 208–214)

### 3.1 Domínio
- `HelpOffer` passa a ter `helpTypes: Set<HelpType>` com **mínimo 1** e
  sem repetição (208).
- Evento `HelpOfferSubmitted` carrega `helpTypes: HelpType[]`; o item da
  linha do tempo `help_offered` idem (212).

### 3.2 Persistência
- Tabela filha `tb_help_offer_type (tb_help_offer_id, help_type, PRIMARY KEY dos dois, CHECK na lista, FK ON DELETE CASCADE)` (209).
- Migração: cria a filha, **backfill** de `tb_help_offer.help_type`
  (uma linha por oferta existente), depois remove a coluna e o CHECK
  antigo (210).

### 3.3 API
- `POST /app-help-offers` recebe `helpTypes: HelpType[]` (1..5, sem
  repetição, 422 `VALIDATION` fora disso); `helpType` singular deixa de
  existir (213).
- Visões (`GET /app-reports/:id` dono/participante, detalhe do painel)
  devolvem `helpTypes: []` por oferta.
- Edição dos tipos depois de ofertar: `PUT /app-help-offers/:id/types
  { helpTypes }`, só pelo helper identificado dono da oferta, só em
  denúncia aberta; substitui o conjunto; item `help_offer_updated` na
  linha do tempo (211/212).

### 3.4 Mobile
- Bloc guarda `Set<HelpType>`; os checkboxes viram de fato múltiplos;
  botão "Enviar" desabilitado com zero marcados.
- Participante identificado vê "Alterar tipos" no detalhe enquanto a
  denúncia está aberta (211).
- Detalhe (dono/participante) lista os tipos separados por " · ".

### 3.5 Painel
- Detalhe do caso lista os tipos por oferta, mesma chave i18n.

## 4. Fatiamento (proposta)
- **HT1 API**: emenda 003/004 → migração → DTO/serviço/repositório →
  visões → testes. ✅ 2026-09-11. Adendo 2026-09-19: facet `myOffer` na
  visão de participante (spec 003/004 emendadas, `reports.md`).
- **HT2 mobile**: bloc/form/detalhe + testes. ✅ 2026-09-19
  (`app/docs/feature/help-offer.md`, seção "Several fronts per offer").
- **HT3 painel**: detalhe do caso + teste (214). ✅ 2026-09-19
  (`app/docs/feature/report-moderation.md`, seção "Several fronts per
  offer").

## Decisões registradas
208 (conjunto de tipos numa oferta) · 209 (tabela filha) · 210 (coluna
antiga removida) · 211 (edição pelo helper identificado em denúncia
aberta) · 212 (um item na linha do tempo, + `help_offer_updated`) ·
213 (só `helpTypes`) · 214 (fatiamento HT1 → HT2 → HT3). Texto integral
no [VGR-plano.md](../decisions/VGR-plano.md).

## Perguntas pendentes
Nenhuma (rodada 16 zerada em 2026-09-11).

## Fora de escopo desta rodada (registrado, não some)
- **Oferta anônima na própria denúncia é aceita** (visto em 2026-09-10:
  oferta 8 na denúncia 4). O veto de autoajuda da decisão 20 só enxerga
  conta; anônimo não tem identidade para comparar. Coerente com a 23
  (anonimato social, não forense); fica registrado como limitação
  conhecida, sem pergunta nesta rodada.
- Peso do tipo de ajuda na recompensa (30c) — nada muda: o split segue
  por recebedor, não por tipo.

## Critérios de sucesso
1. `POST /app-help-offers` com `helpTypes: ['physical_presence','share']`
   grava uma oferta com dois tipos; com `[]` ou repetido responde 422.
2. Dono e participante veem os dois tipos na visão da denúncia; o painel
   também.
3. Ofertas antigas seguem com o tipo que tinham (backfill).
4. Chat, rating e recompensa continuam passando com a suíte atual.
5. No mobile, marcar dois tipos e enviar produz uma oferta com os dois.
