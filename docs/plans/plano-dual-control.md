# Plano — Duplo controle de verdade (decisão 45)

> **Rodada 18 — FECHADA em 2026-10-04** (aberta e zerada no mesmo dia;
> recomendações aceitas nas 4 perguntas). Decisões **223–229** no
> [VGR-plano.md](../decisions/VGR-plano.md). **DC1 API executada em
> 2026-10-04** (api `ea3184f`) e **DC2 painel executada em 2026-10-04**
> (app `eb9d8f1`) — **FRENTE COMPLETA** (§6). Revelação fora (228).
> Pedido de Valdo: "vamos corrigir aprovador dual-control" — o
> achado da PS4 do painel
> ([plano-painel-modelo-setes.md](plano-painel-modelo-setes.md) §9 item 1,
> VGR-RESUMO §6 item 5d). Plano antes de codar; execução fase a fase (38).

---

## 1. Contexto

A decisão 45 diz: nenhum administrador isolado decripta dado de
responsabilização — exige (a) base legal documentada ou emergência
justificada, (b) autorização de pelo menos 2 pessoas distintas e (c) toda
tentativa registrada permanentemente.

O portão foi construído na fase 1 do painel (tarefa 06, API task 31), quando
o painel ainda não tinha sessão: o "aprovador" era um texto qualquer. O
painel tem login com JWT desde as decisões 67/112/114, mas o portão nunca foi
revisto.

## 2. O que está errado hoje (evidência)

| # | Problema | Evidência |
|---|---|---|
| E1 | **O aprovador é o que o corpo da requisição disser.** Um admin com os dois grants posta duas aprovações com ids digitados diferentes e chega sozinho a "2 aprovadores distintos" — o duplo controle vira controle simples. | `api/src/modules/admin-access/dual-control.dto.ts` (`approverId: z.string()` no corpo); `dual-control.controller.ts` (`service.addApproval(id, body.approverId)`); campo `approver-id-field` na tela |
| E2 | Quem ABRIU a solicitação não é registrado. | `tb_dual_control_access_request` (migração 016) não tem `requested_by`; `createRequest` não recebe ator |
| E3 | Nada vai para a trilha administrativa — fere 45(c) e a 116. | o controller não chama `auditFromRequest` (o case-freeze, mesmo padrão de duplo controle, chama) |
| E4 | O id do log de responsabilização não é validado: pede-se acesso a uma entrada que não existe. | `accountability_log_entry_id INT NOT NULL`, sem FK nem checagem |
| E5 | Duas aprovações simultâneas se sobrescrevem (lê o JSON, acrescenta, regrava). | `addApproval` → `findRequestById` + `persistApproval` sem trava |
| E6 | A tela não permite o segundo admin aprovar pela própria sessão: é um fluxo de uma solicitação só, que vive na memória do bloc de quem a criou. | `dual_control_request_page.dart` (`_requestId` no bloc) |
| E7 | Comentário desatualizado: diz que "não existe criptografia" — o log é cifrado em repouso desde a migração 024 (44/111). | `dual-control.interface.ts` |

Contexto que limita o risco HOJE: **nada consome o status `granted`** —
não existe rota que decifre uma entrada do log (o log só é escrito,
`shared/audit/accountability.ts`). O portão protege uma revelação que ainda
não foi construída. Corrigir agora garante que a revelação, quando vier,
encaixe num portão íntegro.

## 3. Correções objetivas (não são escolha — aplicam a 45 e a 116)

- **C1** — Aprovador e solicitante vêm da SESSÃO (`req.user`), nunca do
  corpo; o campo de texto sai da tela (corrige E1, E2).
- **C2** — Abrir e aprovar entram em `tb_admin_audit` (`auditFromRequest`,
  ação `state_change`, entidade `dual_control_access`) — corrige E3.
- **C3** — Solicitação para entrada inexistente do log é recusada (404
  `NOT_FOUND`) — corrige E4.
- **C4** — Corrida (E5) resolvida por escrita condicional (`UPDATE …
  WHERE status = 'pending'`; nenhuma linha afetada = 409). Com a resposta
  1(A) uma aprovação basta, então `approved_by`/`approved_at` na própria
  solicitação substituem a tabela filha pensada aqui (decisão 224); o JSON
  `approver_ids` vira `legacy_approver_ids` (225).
- **C5** — Comentário do E7 corrigido.

## 4. Perguntas da rodada 18 — RESPONDIDAS em 2026-10-04 (decisões 223–229; recomendações aceitas)

1. **Quantas pessoas e quem conta?**
   - (A) Padrão da casa (107, 141d): **quem abre a solicitação já é a
     primeira autorização; UMA aprovação de outra pessoa libera.** Mínimo de
     2 pessoas, mesmo desenho do descongelamento de caso. *(Recomendado)*
   - (B) Duas aprovações de 2 pessoas distintas, podendo o solicitante ser
     uma delas (mínimo 2 pessoas, um clique a mais — o limiar atual).
   - (C) Duas aprovações de 2 pessoas distintas, NENHUMA o solicitante
     (mínimo 3 pessoas).
2. **Solicitações existentes** (aprovadores digitados — não confiáveis):
   - (A) Ficam como histórico com um status novo `void` (anulada: aprovação
     pré-correção), nunca valem como liberadas. *(Recomendado)*
   - (B) Apagadas na migração (dado só de desenvolvimento).
3. **Tela do painel:**
   - (A) Lista paginada das solicitações (mais recentes primeiro, filtro
     por base legal), "Nova solicitação" pelo formulário da fábrica, e
     "Aprovar" na linha — desabilitado para quem já autorizou; mostra quem
     pediu e quem aprovou pelo nome (equipe identificada, nunca e-mail —
     160). Mesmo desenho das regras do Legal Gate. *(Recomendado)*
   - (B) Mantém a tela de uma solicitação só, com busca por id para o
     segundo admin aprovar.
4. **A revelação (decifrar a entrada liberada):**
   - (A) Fica fora desta rodada — o portão fica íntegro agora; a revelação
     espera a revisão jurídica pedida na própria 45 (⚠️ advogado) e terá
     rodada própria (toda tentativa logada, uso único, prazo). *(Recomendado)*
   - (B) Construir a revelação nesta rodada.

## 5. Fatiamento proposto
DC1 API (C1–C5 + decisões da rodada, migração, testes, docs) → DC2 painel
(tela nova, testes, docs). Cada fase por "pode seguir" (38).

| Fase | Conteúdo | Depende de | Estado |
|---|---|---|---|
| **DC1 API** | migração (requested_by, approved_by/at, status `void`, legacy_approver_ids, anulação das existentes); ator da sessão; regra 224; auditoria; 404 na entrada inexistente; lista paginada com nomes; testes; docs da API | rodada 18 | **executada em 2026-10-04** (api `ea3184f`) |
| **DC2 painel** | tela lista + formulário + aprovar na linha (227), sem campo de aprovador; testes; docs do app | DC1 | **executada em 2026-10-04** (app `eb9d8f1`) |

## 6. Execução

### DC1 API — 2026-10-04 (api `ea3184f`, liberada com "pode seguir")

- **Migração 050** (`050_dual_control_session.sql`): `requested_by`,
  `approved_by`, `approved_at` (FK `tb_user`), status `void`,
  `approver_ids` → `legacy_approver_ids`; todas as solicitações existentes
  anuladas (225). Dois CHECKs: solicitação viva sempre tem solicitante;
  `granted` exige aprovador ≠ solicitante — nem um bug no service grava
  liberação de uma pessoa só.
- **Contrato**: `POST /` registra o solicitante da sessão (404 `NOT_FOUND`
  se a entrada do log não existe); `POST /:id/approvals` não tem corpo — o
  aprovador é a sessão; o próprio solicitante recebe 422 `BUSINESS_RULE`;
  pedido não pendente (liberado, anulado ou perdedor de aprovação
  simultânea) recebe 409 `BUSINESS_RULE`, o mesmo código do Legal Gate para
  "não aguarda aprovação". `GET /` paginado sob demanda (220), filtro na
  base legal, mais recentes primeiro, linha com `requestedByName` /
  `approvedByName` (nunca e-mail). Abrir e aprovar gravam `tb_admin_audit`
  (`state_change`, entidade `dual_control_access`).
- **Verificação**: suíte da API 121/121 suítes, 1221 testes; `tsc` limpo.
  Migração e SQL exercitados em **MySQL 8.0 e MariaDB 10.11**: anulação
  das linhas antigas com o JSON preservado, CHECKs recusando auto-aprovação
  e pedido sem solicitante, e duas aprovações simultâneas reais — uma vence,
  a outra recebe 409.
- **Junto, em commit separado** (api `76327dd`): `help-offers.routes.spec`
  não definia o `JWT_SECRET` que usa e só passava quando outra suíte o
  definia antes — 4 testes falhavam rodando sozinhos/na ordem do CI.
- **Achado fora do escopo** (não corrigido): a migração **049** usa
  `DROP CONSTRAINT IF EXISTS` / `DROP COLUMN IF EXISTS`, sintaxe só do
  MariaDB — em MySQL 8.0 ela falha. A cadeia 001–050 roda inteira em
  MariaDB (o dev é MariaDB, por isso a 049 passou em 2026-09-11); a doc diz
  "MySQL". Pendência no VGR-RESUMO §6 (5f).
- **Entre DC1 e DC2** a tela antiga do painel fala o contrato velho
  (`approverIds`, campo de aprovador): não lê as linhas novas. A DC2 a
  substitui.

### DC2 painel — 2026-10-04 (app `eb9d8f1`, liberada com "pode seguir")

- **Tela** `DualControlAccessPage` na fábrica de cadastro, desenho das
  regras do Legal Gate: `RegisterScreen(openRows: false)` + `DualControlBloc`
  (subclasse do `RegisterBloc`, aprovar pelo `act()`). Lista paginada, mais
  recentes primeiro, filtro na base legal; linha com status (aguardando /
  liberada / anulada), base legal, "Pedida por {nome} em …" e "Aprovada por
  {nome} em …" — nome, nunca e-mail; sem nome vira "—".
- **Formulário** espelha o DTO: id da entrada do log
  (`VgrValidators.positiveInteger`, espelho novo de
  `z.number().int().positive()`, decisão 154) e base legal (obrigatória,
  até 500). Nenhum campo de aprovador.
- **Aprovar** só em linha pendente, exige UPDATE da tela + recurso
  `dual_control_approval`, e fica **desabilitado no pedido que você abriu**
  ("outra pessoa precisa aprová-la"). Quem é "você": o `userId` do próprio
  token que a API julga (`sessionUserIdOf` no core) — sem chamada extra;
  só UX, a API continua recusando o solicitante. A aprovação vai com corpo
  vazio; resultado pela ponte e a lista recarrega com a resposta do
  servidor.
- **Verificação**: admin 389 testes, core 61, validadores 102, mobile 428;
  `flutter analyze` limpo. Docs do app: feature doc reescrita, inventário,
  checklist, ARCHITECTURE, README, specs 003/004 do admin emendadas.
- **Observação do painel inteiro** (não é desta frente, não mexido): as
  datas aparecem no horário UTC que a API devolve, sem conversão nem
  rótulo — mesma convenção de 7 telas (auditoria, denúncias,
  estatísticas, congelamento, mediação). Registrado no VGR-RESUMO §6 (5g).

