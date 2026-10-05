# Plano — Pendências 5e/5f/5g (rodada 19)

> **Rodada 19 — FECHADA em 2026-10-04** (aberta e zerada no mesmo dia).
> Decisões **230–233** no [VGR-plano.md](../decisions/VGR-plano.md). R1 e
> R2 liberadas juntas ("pode seguir R1 e R2") e **executadas em
> 2026-10-04** (api `4102afa`, app `5f0ea26`) — **FRENTE COMPLETA** (§4).

---

## 1. Origem

Três pendências do [VGR-RESUMO §6](../decisions/VGR-RESUMO.md), achadas nas
frentes do painel (PS2) e do duplo controle (DC1/DC2):

| Item | Achado | Resposta |
|---|---|---|
| 5e | `PUT /api/users/:id` grava `locale` nulo quando o campo vem ausente; o painel contornava reenviando o valor salvo | "sim" — a API preserva |
| 5f | migração 049 usa `DROP … IF EXISTS` (só MariaDB); a stack dizia "MySQL" | MariaDB |
| 5g | as telas mostram o ISO UTC da API cortado — 3 h adiantado no Brasil | converter para o fuso local |

Esclarecidos na mesma rodada: o mesmo problema de datas existe em 4 telas
do mobile (incluídas — 232) e `active` ausente na edição virava `'S'`
(mesma regra do 5e — 230).

## 2. Decisões

- **230** — edição de usuário: ausente mantém (`locale`, `active`); `null`
  explícito em `locale` limpa.
- **231** — produção em MariaDB; 049 fica; docs dizem MariaDB.
- **232** — API em UTC; painel e mobile no fuso local, formatador único
  no `core` (13 cópias: 9 no painel, 4 no mobile).
- **233** — R1 API → R2 app, liberadas juntas.

## 3. Fases

| Fase | Conteúdo | Estado |
|---|---|---|
| **R1 API** | `userUpdateDto` sem padrão para `active`/`locale`; service mantém o salvo; testes; emenda do spec 004; docs MariaDB (ARCHITECTURE, TESTS, media) | **executada** (api `4102afa`) |
| **R2 app** | formatador de data local no `core` + testes; 9 telas do painel e 4 do mobile migradas; contorno do `locale` no painel removido; docs | **executada** (app `5f0ea26`) |

## 4. Execução

### R1 API — 2026-10-04 (api `4102afa`)

- `userUpdateDto`: `active` e `locale` opcionais, sem padrão; o service
  usa o valor salvo para o que vier ausente; `locale: null` explícito
  limpa. Criação inalterada. A revogação de sessão ao desativar continua
  (agora comparando com o valor efetivo).
- Docs: ARCHITECTURE (fluxo, pool, migrações — MariaDB, sintaxe MariaDB
  permitida), TESTS, media (`GET_LOCK`), dual-control; spec 004 emendado.
- Verificação: 121 suítes, 1227 testes; `tsc` limpo.

### R2 app — 2026-10-04 (app `5f0ea26`)

- `core`: `formatLocalDateTime` / `formatLocalDate`. Só converte valor com
  fuso (`Z` ou `±hh:mm`); data pura ou sem fuso aparece como veio.
  Conferido: `21:38Z` aparece `18:38` em America/Sao_Paulo.
- 13 cortes de string UTC trocados pelo formatador (9 telas do painel, 4
  do mobile — o `formatChatTime` do chat incluído). Os baldes de tempo do
  chat (174: 1 min / 15 min / 1 h) sobrevivem à conversão.
- **Achado no caminho**: 10 testes fixavam o horário UTC no texto
  esperado — passavam no CI (UTC) e **falhariam numa máquina no Brasil**.
  Agora esperam a saída do formatador; admin, mobile e core passam em UTC,
  America/Sao_Paulo e Asia/Kolkata. Regra nova no `TESTS.md`.
- Painel: a edição de usuário deixou de reenviar `locale` (230) — o que
  também evita sobrescrever um idioma que o usuário acabou de trocar.
- Verificação: admin 389, mobile 428, core 67 nos três fusos; analyzer
  limpo.
