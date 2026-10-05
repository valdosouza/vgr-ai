# Plano — Mediação no menu e filtros de data (rodada 20)

> **Rodada 20 — FECHADA em 2026-10-04** (aberta e zerada no mesmo dia).
> Decisões **234–236** no [VGR-plano.md](../decisions/VGR-plano.md).
> **M1 e M2 aguardam "pode seguir".**

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
| **M1 API** | migração 051 (`reward_mediation` kind 'T'); teste da árvore do menu; docs (reward, access-control, admin-audit/menu) | aguarda "pode seguir" |
| **M2 painel** | função de intervalo local → UTC no `core` + testes em mais de um fuso; auditoria e busca de denúncias passam a usá-la; inventário do painel (mediação no menu); docs | aguarda "pode seguir" |

## 4. Fica registrado

- **Estatísticas de denúncias**: os baldes (dia/semana/mês) são cortados em
  UTC pela API. Mostrar baldes no dia local pediria um parâmetro de fuso na
  API — não decidido nesta rodada.
