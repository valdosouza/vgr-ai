# Plano — Contrato de erro da API (decisão 80)

> A API responde erro somente em inglês; quem traduz é o cliente, pela chave do
> `code`. Este plano lista o que precisa mudar para que o `code` realmente sirva
> como chave de tradução — hoje ele não serve.
>
> Data: 2026-08-03 · Status: **EXECUTADO** em 2026-08-03 · Decisões 80 e 83 ·
> Verificado: `tsc --noEmit` limpo, 22 suítes / 112 testes passando.
>
> A decisão 83 (erro por campo traduz por código) fechou a pendência aberta em
> §2.3 e foi implementada junto — `FieldErrorCodes`, `fields[].code`,
> `params` estruturados, `HttpError.code` obrigatório e os 9 call sites
> reclassificados. Este documento fica como registro do porquê.

---

## 1. O que já está certo

Varredura completa em `api/src`: **nenhuma mensagem de erro em português**. O
padrão `{ error, code?, fields? }` existe, `handleError` é único e centralizado,
`error-codes.ts` existe. A decisão 80 não exige nenhuma correção de idioma.

## 2. O que a decisão 80 quebra

Ao dizer "o cliente traduz pelo `code`", o `code` deixa de ser um detalhe de
diagnóstico e vira **contrato de interface**. Três problemas surgem daí.

### 2.1 Códigos colididos — o cliente traduziria errado

Cinco erros 409 semanticamente distintos carregam `DUPLICATE` hoje:

| Local | Mensagem | `code` hoje | `code` proposto |
|---|---|---|---|
| `interfaces/interface.service.ts:46` | Interface has user privilege grants | `DUPLICATE` | `IN_USE` |
| `privileges/privilege.service.ts:44` | Privilege is in use by interfaces or user grants | `DUPLICATE` | `IN_USE` |
| `users/user.service.ts:58` | You cannot delete your own account | `DUPLICATE` | `SELF_LOCKOUT` |
| `users/user.service.ts:129` | You cannot revoke your own access to the Users screen | `DUPLICATE` | `SELF_LOCKOUT` |
| `admin-access/dual-control.service.ts:25` | This approver has already approved | `DUPLICATE` | `DUPLICATE` ✔ mantém |

O caso mais visível é o terceiro: o app renderizaria "já existe" quando o Admin
tenta apagar a própria conta. `DUPLICATE` continua correto nos seis usos legítimos
(e-mail já em uso, chave de interface já existe, privilégio já existe).

Mesma colisão em 422, entre validação de payload e regra de negócio:

| Local | Mensagem | `code` proposto |
|---|---|---|
| `identity/identity.service.ts:25` | identified_with_reward requires completed registration | `BUSINESS_RULE` |
| `identity/identity.service.ts:40` | Cannot transition from anonymous to X | `BUSINESS_RULE` |
| `users/user.service.ts:108` | Privilege is not cataloged for this interface | `BUSINESS_RULE` |
| `identity/identity.service.ts:15,22` | Invalid role / Invalid anonymity mode | `VALIDATION_FAILED` ✔ mantém |
| `system-modules/system-module.service.ts:20` | One or more interfaces do not exist | `VALIDATION_FAILED` ✔ mantém |

Menor, mas do mesmo tipo: `identity.service.ts:37` ("Role transition to police is
deferred — decisão 12") usa `FORBIDDEN`, mas não é falta de permissão e sim
funcionalidade adiada. Sugestão: `NOT_AVAILABLE`.

### 2.2 Mensagens com valor interpolado perdem o valor na tradução

`Invalid role: ${value}` e `Cannot transition from anonymous to ${targetRole}`
embutem o dado no texto inglês. Se o cliente traduz pela chave, o parâmetro
some. Valor interpolado precisa viajar estruturado — em `fields[]` ou num
`params` novo — nunca só dentro da string.

### 2.3 Erro por campo não tem código nenhum ⚠️

`zodToFields` (`shared/http/controller-utils.ts:42`) coloca a **mensagem crua do
Zod** em `fields[].message`. Não há `code` por campo. Ou seja: toda validação de
formulário — o erro que o usuário mais vê — é intraduzível pelo contrato da
decisão 80, e o admin/app exibiria inglês do Zod.

Isto é maior que um item de execução e virou pergunta da rodada (pendência 3 da
rodada 1 em `VGR-plano.md`).

## 3. Mudanças propostas — todas aplicadas ✔

1. **`error-codes.ts`**: acrescentar `IN_USE`, `SELF_LOCKOUT`, `BUSINESS_RULE`,
   `NOT_AVAILABLE`.
2. **`HttpError.code`**: deixar de ser opcional (`code?: string` → `code: string`).
   O compilador passa a garantir o que hoje é convenção; `handleError` perde o
   `...(err.code ? ... : {})`.
3. **Reclassificar os 9 call sites** das tabelas de §2.1.
4. **Parâmetros estruturados** nos dois erros interpolados de §2.2.
5. **Testes**: os `*.spec.ts` que afirmam `code: 'DUPLICATE'` nos 4 call sites
   reclassificados mudam junto — é mudança de contrato, os testes devem sentir.

Custo estimado: uma sessão. Nada disso muda status HTTP nem quebra o app (que
ainda não consome os códigos — daí a janela para fazer agora).

## 4. Ordem

Depois da rodada 1 fechar (pendência 3 decide o §2.3) e **antes da Fase 4**
(telas admin) do `plano-controles-administrativos.md` — é a primeira frente que
vai efetivamente traduzir mensagens de erro na interface.
