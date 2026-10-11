# Plano — Identificação do helper: escolha explícita, oculto por padrão (rodada 21)

> **Rodada 21 — FECHADA em 2026-10-05** (aberta e zerada no mesmo dia).
> Decisões **237–239** no [VGR-plano.md](../decisions/VGR-plano.md).
> H1 e H2 liberadas juntas ("pode seguir") e **executadas em 2026-10-05**
> (api `4b6d658`, app `fd2513f`): **FRENTE COMPLETA** (§5).

---

## 1. Origem

O teste do app mobile no navegador (VGR-RESUMO §6, 5i) mostrou que um
helper com conta oferecia ajuda **sempre identificado**. O app mandava
`anonymous: false` sempre que havia sessão, e a API tratava `anonymous`
ausente como identificado. A escolha que a 170 pressupõe ("nome só quando
ele escolheu identificar-se") nunca tinha sido construída. O tier high já
saía sem nome, porque o servidor corta.

Valdo: "imagine um traficante criando uma denúncia falsa, tentando
identificar algum helper que está ajudando para intimidá-lo… temos que
garantir a segurança de quem denuncia e de quem ajuda para casos
críticos". E ao esclarecer: "passar por análise seria avaliar a categoria
de risco, como é feito com o denunciante".

## 2. Decisões

- **237**: identificar-se é escolha EXPLÍCITA do helper e o padrão é
  oculto. A API trata `anonymous` ausente como oculto. O helper oculto
  continua identificável pela plataforma (60), pode conversar, ser
  avaliado e receber recompensa.
- **238**: o nome passa pela análise da categoria de risco, como o
  denunciante. Em risco alto o nome nunca aparece, nem que o helper queira,
  e o app nem oferece a opção, só o aviso. Nos demais níveis a opção
  aparece desmarcada. Nenhum administrador libera nome caso a caso.
- **239**: H1 API → H2 mobile, cada uma por "pode seguir".

## 3. Fases

| Fase | Conteúdo | Estado |
|---|---|---|
| **H1 API** | `anonymous` ausente = oculto em `POST /app-help-offers`; testes de rota; docs (reports, specs 003/004) | **executada** (api `4b6d658`) |
| **H2 mobile** | caixa "Mostrar meu nome a quem denunciou" desmarcada com aviso (risco baixo/médio); só o aviso em risco alto; nível desconhecido fecha em oculto; textos pt/en; testes; docs | **executada** (app `fd2513f`) |

## 4. Fica registrado

- **Ofertas gravadas antes da rodada 21**: as ofertas de helpers com conta
  feitas até aqui ficaram gravadas como identificadas sem que ninguém
  tivesse escolhido. Hoje só existem dados de teste (banco local). Se já
  houver dados reais quando o app for para produção, decidir se essas
  ofertas passam a ocultas.

## 5. Execução — 2026-10-05

### H1 API (api `4b6d658`)
- `submitHelpOfferDto`: `anonymous` passa de `default(false)` para
  `default(true)`. Sem sessão a oferta continua sempre oculta (35). O corte
  do tier high (40/60) já existia e não mudou: visão do denunciante
  (`reports.service`) e máscara do chat (170).
- A recompensa usa a conta e não o sinal de oculto (`reward.service`). Por
  isso uma oferta oculta com conta continua podendo receber recompensa
  (60), e a avaliação também continua (180).
- Testes: helper com conta que não manda escolha fica oculto (falha sem a
  correção); helper com conta só é nomeado com `anonymous: false`. Suíte
  121/121, 1229 testes; `tsc` limpo.

### H2 mobile (app `fd2513f`)
- A tela de detalhe passa o nível da denúncia ao formulário de oferta.
  - **Risco baixo ou médio**: aparece a caixa "Mostrar meu nome a quem
    denunciou", desmarcada, com o aviso "Na dúvida, deixe desmarcado: uma
    denúncia pode ser falsa, feita só para descobrir quem ajuda. Sem o nome
    você continua podendo conversar, ser avaliado e receber recompensa."
  - **Risco alto**: nenhuma caixa, só "Caso de risco alto: seu nome nunca é
    mostrado a quem denunciou nem a outros helpers, mesmo que você queira."
  - **Nível desconhecido** (link direto, sem o nível): a oferta vai oculta.
- O link para se cadastrar e receber recompensa continua aparecendo para
  todo helper com conta, oculto ou não. A tela de alterar tipos de ajuda
  (211) não mexe no nome.
- Testes: +5 no formulário (4 falham na versão anterior). Mobile 433, todos
  verdes; analyzer limpo.

### Conferido no navegador
Banco MariaDB local, API da branch, app compilado. O denunciante abriu três
denúncias: 4 = Atividade suspeita (risco baixo), 5 = Roubo / furto (médio)
e 6 = Sequestro (alto). Carlos, helper com conta, ofereceu ajuda nas três:

| Denúncia | O que o formulário mostrou | O que foi enviado | O denunciante viu |
|---|---|---|---|
| 4 (baixo) | caixa desmarcada + aviso; não marcou | `anonymous: true` | "Helper anônimo" |
| 5 (médio) | caixa desmarcada + aviso; marcou | `anonymous: false` | "Carlos Helper" |
| 6 (alto) | sem caixa, só o aviso de risco alto | `anonymous: true` | "Helper anônimo" |

Nas três, a tela de sucesso manteve o link para se cadastrar e receber
recompensa.
