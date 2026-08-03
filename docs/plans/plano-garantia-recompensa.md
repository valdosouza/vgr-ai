# Plano — Garantia da recompensa: retenção, selo e mediação

> Como reter o valor da recompensa de modo que o helper possa ser pago, o
> denunciante possa ser reembolsado em alguns casos, e exista mediação — **sem**
> o VGR virar custodiante e sem quebrar a decisão 84.
>
> Data: 2026-08-03 · Status: análise para decisão (item 9 da rodada 3) ·
> Decisões envolvidas: 30, 39, 58, 81, 82, 84, 85, 86

---

## 1. A tensão que precisa ser resolvida primeiro

O pedido tem três partes que, ditas juntas, se contradizem:

1. *"A plataforma é apenas intermediadora, não podemos garantir recebimento."*
2. *"Selo: Garantia 30 dias / Garantida 100%."*
3. *"Reter o valor, devolver ao denunciante em alguns casos, com mediação."*

**(1) e (2) não convivem.** Se o app estampa "Garantida 100%", quem garante é o
VGR — e no Brasil a oferta publicitária vincula quem a faz (CDC, arts. 30 e 35).
Um disclaimer nos termos de uso não desfaz o que o selo prometeu na tela. Ou o
valor está realmente retido e a plataforma realmente o libera — e aí ela **está**
assumindo uma obrigação, não apenas intermediando — ou não está, e o selo não
pode dizer "garantida".

**(3) é possível sem quebrar a decisão 84**, e é aí que está a saída: *reter* e
*custodiar* não são a mesma coisa. O que a decisão 84 proíbe é o VGR ser
**titular** do dinheiro. Existe retenção em que o titular é outro e o VGR apenas
**instrui a liberação** — isso é papel de mediador, não de custodiante.

## 2. Os três mecanismos, e o que cada um custa

### A. Pré-autorização (bloqueio no emissor) — decisão 85

O valor nunca sai da conta do denunciante; o emissor do cartão bloqueia o
limite. Resolver = capturar (dinheiro anda direto para o split). Não resolver =
cancelar a autorização, e o limite volta sozinho, **sem fluxo de estorno**.

- Custódia: **zero**. O dinheiro literalmente não existe em lugar nenhum até a
  captura. Decisão 84 intacta, sem depender de como o PSP organiza contas.
- Devolução ao denunciante: automática e instantânea (é só não capturar).
- Mediação: possível — o VGR decide entre capturar e cancelar.
- ⚠️ Limite: a janela. Pré-autorização de cartão vive tipicamente entre 5 e 30
  dias, dependendo de bandeira e adquirente. Não dá para prometer mais que isso.
- ⚠️ Limite: é recurso de **cartão**. Pix não tem pré-autorização equivalente
  (o helper continua recebendo por Pix/transferência — decisão 82 —, o que muda
  é o instrumento do *pagador*). Confirmar o estado atual disso na pesquisa da
  decisão 59; é área que muda rápido.

### B. Retenção no PSP (o dinheiro sai, mas fica preso lá)

O denunciante paga na oferta; o valor liquida no PSP e fica retido até o VGR
mandar liberar para o helper ou devolver.

- Custódia: **depende do PSP, e é preciso verificar caso a caso.** Se a retenção
  acontece em conta titularizada pelo marketplace (é assim que vários
  implementam), o VGR vira titular de dinheiro de terceiro e a decisão 84 cai —
  com ela, a isenção da decisão 81 e o BACEN de volta. Se o titular é o próprio
  PSP na sua capacidade regulada, ou o recebedor com saldo bloqueado, a
  decisão 84 se mantém.
- Prazo: **sem janela**. É o que permite prometer reserva até a resolução.
- Devolução: exige fluxo de estorno de verdade (prazo, taxa, e o denunciante
  passa um tempo sem o dinheiro).
- Mediação: plena.

### C. VGR retém

Proibido pela decisão 84 e exige autorização do BACEN. É o conteúdo da
capacidade `reward.intermediation.own`, bloqueada no Legal Gate (decisão 81).
Não é escolha de arquitetura hoje; é projeto regulatório.

## 3. Os dois selos pedidos mapeiam nos dois mecanismos

Isto encaixa melhor do que parecia:

| Selo pedido | Mecanismo | O que pode honestamente dizer |
|---|---|---|
| "Garantia 30 dias" | **A** — pré-autorização | *Valor reservado até DD/MM* — prazo explícito, porque a janela é real |
| "Garantida 100%" | **B** — retenção no PSP | *Valor reservado até a resolução* — sem prazo, se e somente se a titularidade for verificada |
| (sem selo) | nenhum | *Recompensa sem reserva* — e a decisão 86 exige ciência do helper |

A palavra "garantida" continua sendo o problema, não o conceito. **"Valor
reservado" descreve exatamente o que existe** — dinheiro separado, liberação
condicionada — sem prometer um resultado que estorno e chargeback ainda podem
desfazer. E resolve a contradição do §1: a plataforma não garante *recebimento*,
ela garante *reserva*. São coisas diferentes e a segunda é verdade.

## 4. Mediação — o que ela é e o que ela cria

Mediar é decidir se a condição da promessa foi cumprida (decisão 30) e, com
isso, se o valor vai ao helper ou volta ao denunciante. Consequências:

- **É papel administrativo**, mora no `apps/admin` e usa o modelo de privilégio
  da decisão 71/72. O padrão de duplo controle da decisão 45 é o candidato
  natural para liberações acima de um valor.
- **Os critérios têm de ser públicos e anteriores ao caso.** Mediador que decide
  por critério não declarado é fonte de reclamação; declarado, é regra do jogo.
- **A decisão precisa ser registrada e contestável** — mesmo padrão de log
  imutável do Legal Gate (decisão 76).
- ⚠️ **Mediação é o que mais aproxima o VGR de "prestar serviço de pagamento".**
  Instruir liberação de dinheiro retido de terceiro, cobrando taxa por isso, é
  atividade que merece checagem específica na análise do Legal Gate — e é
  exatamente o tipo de capacidade que a decisão 77 manda declarar por país em
  vez de presumir. Sugestão: capacidade nova `reward.mediation`.

## 5. Decidido — e depois simplificado pela decisão 95

A decisão 87 escolheu os dois mecanismos, por faixa. **A decisão 95 tirou o
cartão de crédito do escopo** ("a ideia é ajudar pessoas, não criar passivo para
a empresa"), e com ele o mecanismo A: pré-autorização é recurso de cartão.

**Resta um mecanismo: B, retenção no PSP, alimentada por Pix.** O denunciante
que quer o selo retém o valor; quem não retém oferta sem selo (decisões 85, 88).

O que a simplificação apagou, e é muito: a janela de 5 a 30 dias e todo o fluxo
de renovação (decisões 89, 90), a espera longa do helper por causa de
contestação (decisão 94), e a exposição a chargeback que motivou as decisões 92
e 93. Pix é irrevogável — o passivo que essas decisões administravam
simplesmente não nasce.

O que a simplificação agravou, e é um só ponto, mas grande: **a verificação de
titularidade virou dependência bloqueante.** Enquanto havia o mecanismo A, um
PSP que só retivesse em conta do marketplace apenas eliminava B. Agora elimina o
selo inteiro — ou a decisão 84. Sobe ao topo da pesquisa da decisão 59.

Consequência para o código: `PaymentRail` (ACL do Reward, decisão 81) expõe
`reserve` / `capture` / `cancel` com **uma** implementação. A porta continua
justificada — é o que permite o trilho próprio futuro (decisão 81) e outro país
com outro rail (decisão 68) sem tocar no domínio.

## 6. O que isto ainda não resolve

- **Titularidade do valor retido** e **prazo máximo de retenção** (item 17) —
  não são escolhas nossas, são fatos a apurar com o PSP, e o primeiro é
  bloqueante.
- O texto do selo (item 7 da rodada 3) — agora é **um só**, o que simplifica;
  continua valendo que "garantida" promete recebimento e a plataforma só pode
  prometer reserva.
- A fricção que o Pix traz e o cartão não trazia: o dinheiro sai de verdade na
  oferta, então denúncia não resolvida exige devolução, não cancelamento.
