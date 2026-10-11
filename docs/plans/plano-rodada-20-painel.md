# Plano — Mediação no menu e filtros de data (rodada 20)

> **Rodada 20 — FECHADA em 2026-10-04** (aberta e zerada no mesmo dia).
> Decisões **234–236** no [VGR-plano.md](../decisions/VGR-plano.md).
> M1 e M2 liberadas juntas ("pode seguir") e **executadas em 2026-10-04**
> (api `e825bf1`, app `6ff4a61`) — **FRENTE COMPLETA** (§5).

---

## 1. Origem

O teste do painel no navegador (VGR-RESUMO §6, 5h — app `fdf8e34`) deixou
dois pontos para decisão:

| Ponto | Achado | Resposta |
|---|---|---|
| (a) | A tela de mediação de recompensa só abria pela URL: `reward_mediation` é recurso kind 'R' (migração 035), fora do menu, e nenhuma tela linka para ela | entra no menu |
| (b) | Os filtros de data iam como dia UTC, enquanto as datas na tela são locais desde a 232 — perto da meia-noite uma linha cai fora do dia digitado | o painel converte |

## 2. Decisões

- **234** — `reward_mediation` vira tela kind 'T' em Operações, depois de
  Configuração de Monetização; guard da API inalterado.
- **235** — o dia digitado é o dia local; o painel manda `from` = 00:00
  local e `to` = 23:59:59.999 local, ambos em ISO UTC. Auditoria e busca de
  denúncias; estatísticas fora (baldes UTC na API).
- **236** — M1 API → M2 painel, cada uma por "pode seguir".

## 3. Fases

| Fase | Conteúdo | Estado |
|---|---|---|
| **M1 API** | migração 051 (`reward_mediation` kind 'T'); menu conferido na API; docs (reward, access-control) | **executada** (api `e825bf1`) |
| **M2 painel** | função de intervalo local → UTC no `core` + testes em mais de um fuso; auditoria e busca de denúncias passam a usá-la; inventário do painel (mediação no menu); docs | **executada** (app `6ff4a61`) |

## 4. Fica registrado

- **Estatísticas de denúncias**: os baldes (dia/semana/mês) são cortados em
  UTC pela API. Mostrar baldes no dia local pediria um parâmetro de fuso na
  API — não decidido nesta rodada.

## 5. Execução — 2026-10-04

### M1 API (api `e825bf1`)
- Migração 051: `UPDATE tb_interface SET kind = 'T'` em `reward_mediation`
  — o mesmo movimento que a 034 fez para `case_freeze`. Mesma linha, mesmos
  grants, mesmos guards.
- Conferido em MariaDB: `GET /api/core/menus` de uma admin com todos os
  grants lista `reward_mediation` em Operações, depois de
  `monetization_config`. A 034 também não tinha spec (migração só de
  dado); a prova é o menu real. Comentários de `privileges.ts` corrigidos
  (`REWARD_MEDIATION` e `CASE_FREEZE` ainda diziam kind 'R').
- Suíte da API 121/121, 1227 testes; `tsc` limpo.

### M2 painel (app `6ff4a61`)
- `core`: `localDayStartUtc` / `localDayEndUtc` — 00:00 e 23:59:59.999 do
  dia LOCAL, em ISO UTC; o fim parte da próxima meia-noite local (dia com
  horário de verão fecha certo); data impossível dá nulo. Testado em UTC,
  São Paulo, Kolkata e Nova York.
- Auditoria e busca de denúncias convertem na borda (`toQueryParameters`);
  o formulário guarda o dia digitado. A API não mudou.
- **Conferido no navegador** (fuso São Paulo): uma linha de auditoria
  gravada às 00:00 UTC de 5/10 (21:00 local de 4/10) aparece ao filtrar o
  dia local 2026-10-04 — com o dia "puro" ela ficaria de fora; e
  "Mediação de Recompensa" aparece em Operações e abre a tela.
- Testes: admin 392 em três fusos, core 71, mobile 428; analyzer limpo.
