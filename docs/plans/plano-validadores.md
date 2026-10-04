# Plano — Validadores compartilhados do app (`packages/vgr_validators`)

> **Rodada 10 — FECHADA em 2026-09-02** (rodada 0 organizada e rodada 1
> decidida no mesmo dia). Nasceu do gap 4 da auditoria TDD de 2026-08-22.
> Decisões **153–157** registradas no [VGR-plano.md](../decisions/VGR-plano.md).
> **Executada em 2026-09-02**: API `d593fd0`, app `d85e3df`. Critérios
> do §9 todos atendidos.

---

## 1. Contexto

`packages/vgr_validators` existe no workspace desde o esqueleto do app
(espelho de `setes-app/packages/setes_validators`, decisões 15–17), é
dependência declarada de `apps/mobile` e `apps/admin`, e o cabeçalho do seu
`pubspec.yaml` promete:

> "shared validators for the app: mirrors `src/shared/validation` in
> vgr-api — keep the rules IDENTICAL on both sides (API = source of truth).
> No widgets, no easy_localization, no API calls: pure functions + mask
> TextInputFormatter."

**Estado real (evidência, 2026-09-02):**

| O que | Onde | Achado |
|---|---|---|
| Conteúdo do pacote | `packages/vgr_validators/lib/vgr_validators.dart` | Só o `Calculator.addOne` do template `flutter create`. Teste: `addOne(2)==3`. |
| Consumidores | `grep vgr_validators --include=*.dart apps packages` | **Zero imports** fora do próprio teste. |
| Espelho prometido na API | `api/src/shared/validation` | **Não existe.** A API valida com Zod inline por DTO (`account.dto.ts`, `reward.dto.ts`, …); não há módulo compartilhado de regras. |
| Validação de formulário no mobile | `reward_onboarding_page.dart:58` | `_validate()` local: só "obrigatório" + `num.tryParse` da renda. taxId, telefone e CEP passam **sem formato** (a API exige 11–14, 10–13 e 8–9 caracteres). |
| | `register_page.dart:41`, `login_page.dart:34` | **Nenhuma** pré-validação: e-mail e senha vão direto ao bloc; quem rejeita é a API (422 com `code` por campo, decisão 83). |
| | `report_form_page.dart:58` | Pré-validação offline pelo catálogo (decisão 47) — regra de domínio, não de formato. |
| Validação no admin | `case_freeze_page.dart:48`, `legal_rules_page.dart:59`, `legal_capabilities_page.dart:30` | `length < N` inline, sem mensagem de campo. |
| Máscara/formatação | `packages/vgr_widgets/lib/src/vgr_field.dart:50` | Só `digitsOnly` quando `keyboard == number`. Nenhuma máscara de CPF/telefone/CEP em lugar nenhum. |
| Referência (setes) | `setes_validators/lib/src/validators.dart` | `compose/required/minLength/maxLength/onlyDigits/onlyLetters/cpf/cnpj/cep/phoneBr/email/mask` + `SetesMaskFormatter` + `unmask`. Espelha `setes-api/src/shared/validation/validators.ts`. |

**Leitura:** a hipótese da auditoria ("validações duplicadas e sem teste
espalhadas pelos blocs") **não se confirmou**. O que existe é o oposto:
**quase nenhuma validação de formato no cliente** — o app confia no 422 da
API. Isso é coerente com dois invariantes já vigentes:

- decisão 83: o `code` do erro por campo é o contrato de i18n, então a tela
  já sabe mostrar erro de campo vindo do servidor;
- decisão 123 ("a denúncia nunca espera"): fricção mínima antes de enviar.

O que **não** é coerente é ter um pacote morto no workspace com um
cabeçalho que promete um espelho inexistente, e o guard 133 não cobrindo
nada disso.

## 2. Objetivos (confirmados pelas decisões 153–157)

1. O workspace não carrega pacote sem função (ou ele tem conteúdo, ou sai).
2. Toda regra de formato que exista no cliente é **idêntica** à da API e
   testada nos dois lados (invariante 5: spec vinculante, emenda antes de
   divergir).
3. A tela nunca reimplementa regra de formato inline — se existe regra no
   cliente, ela vive em um único lugar (mesma lógica da decisão 133 para
   widgets e da 143 para provedores).

## 3. Alternativas que estavam em cima da mesa (escolhida: **C**, decisão 153)

### (A) Descontinuar o pacote
Remover `packages/vgr_validators` do workspace e dos dois `pubspec.yaml`.
Validação de formato fica **só na API** (Zod), o cliente exibe o `code`
por campo (83). Mantém-se a validação de *domínio* local que já existe
(catálogo do report, decisão 47; "obrigatório" do onboarding).

- Prós: zero código novo; coerente com o que o app já faz hoje; sem risco
  de divergir regra entre app e API.
- Contras: usuário só descobre CPF/telefone/CEP inválido após round-trip;
  na fila offline (28) o erro chega horas depois; sem máscara de digitação.

### (B) Construir o pacote agora, espelhando um `shared/validation` novo na API
Criar `api/src/shared/validation` (Zod reutilizável: `cpfSchema`,
`brPhoneSchema`, `cepSchema`, …), migrar os DTOs a usá-lo, e implementar
`vgr_validators` com as **mesmas** regras + `VgrMaskFormatter` (padrão do
setes). Migrar `reward_onboarding_page` e as páginas do admin. Ampliar o
guard 133 para proibir `RegExp(`/`.length <` de formato em `presentation/`.

- Prós: feedback imediato e máscaras; regra única declarada nos dois lados;
  fecha o cabeçalho do pubspec como verdade.
- Contras: é uma frente real (API + app + guard + testes); toca DTOs já
  entregues; hoje só o onboarding do helper tem campo com formato BR.

### (C) Construir mínimo, sob demanda
Manter o pacote, trocar o `Calculator` por **só o que o onboarding do
helper precisa hoje** (CPF/CNPJ, telefone BR, CEP, e-mail) + máscara,
espelhando as regras que a API já aplica em `reward.dto.ts` (sem criar
`shared/validation` na API agora — só garantir por teste que a regra do
app é ≥ tão restritiva quanto o Zod). Sem guard novo.

- Prós: menor que (B), já entrega valor onde há campo BR; pacote deixa de
  ser morto.
- Contras: "espelho" vira compromisso de disciplina, não de código —
  invariante 5 fica frágil; risco de o app aceitar o que a API rejeita
  ou vice-versa.

## 4. O que já é invariante e não volta à mesa

- A API **sempre** revalida (47, 110). Validação de cliente é conforto, não
  segurança — nunca substitui o Zod.
- Erro de campo vem por `code` (83); mensagem traduzida é da tela, nunca
  do validador (mesma regra de `VgrDropdownField`: "o design system nunca
  traduz nada").
- Nada de SDK/pacote de validação de terceiros direto na tela (133/143).

## 5. Entregáveis (coluna **C** é a escolhida — decisão 153)

| Item | Se A | Se B | Se C |
|---|---|---|---|
| Remoção do pacote + pubspecs | ✅ | — | — |
| `api/src/shared/validation` + migração dos DTOs | — | ✅ | — |
| `vgr_validators` com regras + `VgrMaskFormatter` + testes | — | ✅ | ✅ (subconjunto) |
| Migração `reward_onboarding_page` (+ admin) | — | ✅ | ✅ (só onboarding) |
| API: `taxId`/`payerTaxId` com dígito verificador em `reward.dto.ts` | — | ✅ | ✅ (decisão 155) |
| `VgrTextField.mask: VgrMask?` em `vgr_widgets` | — | ✅ | ✅ (decisão 157) |
| Guard 133 ampliado (regra de formato inline proibida) | — | ✅ | ❌ (decisão 156) |
| Feature doc `app/docs/feature/validators.md` | — | ✅ | ✅ |
| Emenda no `VGR-RESUMO.md` §4 e §6 | ✅ | ✅ | ✅ |

## 6. Decisões registradas

Texto integral no [VGR-plano.md](../decisions/VGR-plano.md), seção
"Validadores compartilhados do app (rodada 10)".

- **153** — pacote construído no mínimo, sob demanda (opção C); B fica
  como evolução, A recusada por causa da fila offline (28).
- **154** — verdade da regra é o Zod inline do DTO; teste do app cita o
  DTO espelhado, borda por borda.
- **155** — CPF/CNPJ com dígito verificador nos dois lados; API endurece
  `reward.dto.ts`; app envia só dígitos.
- **156** — guard contra validação inline em tela adiado (vai com B).
- **157** — formatter de máscara em `vgr_validators`; `VgrTextField`
  ganha `mask: VgrMask?`; tela só passa o enum.

## 7. Pendências (rodada 10 — validadores)

**Nenhuma.** Itens 1–5 resolvidos em 2026-09-02 pelas decisões 153–157
(respostas: 1C, 2ii, 3ii, 4iii, 5i).

## 8. Fora de escopo desta rodada

- **Opção B** (módulo `api/src/shared/validation` + migração de todos os
  DTOs + guard de validação inline em tela, decisões 153/156): reabrir
  quando surgir o segundo formulário com campo de formato.
- As três telas do admin com `length < N` inline (156) — ficam.
- Validação de domínio (catálogo do report, decisão 47) — já resolvida,
  não é formato.
- Validação de senha no cliente — política única na API (124); o app só
  mostra o `code`.
- i18n das mensagens — é da tela (83), nunca do validador.

## 9. Critérios de sucesso

1. `packages/vgr_validators` não contém nenhuma linha do template
   `flutter create`; exporta CPF/CNPJ, telefone BR, CEP, e-mail,
   `unmask` e `VgrMaskFormatter` (153, 157).
2. Cada validador tem comentário `// mirrors ...dto.ts` e teste por borda
   (mínimo, máximo, dígito verificador válido/inválido) (154, 155).
3. `reward.dto.ts` rejeita CPF/CNPJ com dígito verificador errado, com
   teste (155); `reward_onboarding_page` valida formato local e envia só
   dígitos.
4. `VgrTextField` aceita `mask:` e a tela do onboarding não importa nada
   de `flutter/services` (157, guard 133 verde).
5. `flutter test` dos dois apps e `npm test` da API verdes.
6. `VGR-RESUMO.md` §4 ganha a linha da frente e §6 perde o gap da
   auditoria; `app/docs/feature/validators.md` escrita.
