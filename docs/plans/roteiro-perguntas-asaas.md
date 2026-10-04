# Roteiro de perguntas ao Asaas — confirma B2–B5/D1 e fecha (ou elimina) o candidato

> Para enviar ao comercial/suporte do Asaas (ou levar a uma call). Cada pergunta
> mapeia um item ainda aberto do [plano-psp-requisitos.md](plano-psp-requisitos.md);
> as respostas entram lá como **fatos** (§4) e decidem se o candidato vira a
> decisão 59. O que já está confirmado por documentação pública (B1 —
> titularidade na subconta do recebedor; D2 — consulta do estado vivo por
> `GET /payments/{id}/escrow`; D6 — sandbox) não precisa ser reperguntado,
> só validado de passagem.
>
> Data: 2026-08-21 · Status: pronto para envio · Origem: decisões 30, 58, 82,
> 84, 92, 95, 100, 102 e checklist da decisão 59.

---

## Contexto a apresentar antes das perguntas

Somos um marketplace facilitador: o pagador paga por Pix, o valor deve ficar
**retido na subconta do recebedor** (Conta Escrow) até a plataforma instruir o
desfecho — liberar ao(s) recebedor(es) ou devolver ao pagador. A plataforma
**nunca** é titular do valor; nossa taxa entra como perna do split. Precisamos
confirmar como split, escrow e estorno se compõem numa mesma cobrança.

*Não* mencionar a natureza do produto (denúncias/recompensas) além do
necessário nesta fase — a pergunta é técnica/contratual; enquadramento
jurídico do produto é assunto do Legal Gate, não do PSP.

## Bloco 1 — eliminatórias (um "não" elimina o Asaas)

**P1 (B2/B3 — split + escrow na mesma cobrança).** Uma cobrança Pix criada com
`split[]` (N `walletId`s, valores fixos) em que o recebedor tem Conta Escrow
ativa: o valor das pernas do split fica retido no escrow de cada recebedor até
o `finish`? Split e escrow **compõem na mesma cobrança**, ou são produtos
mutuamente exclusivos? Há limite de N recebedores por split?

- Resposta que aprova: compõem; cada perna retida na subconta do seu recebedor.
- Resposta que elimina: não compõem, ou escrow só sem split.

**P2 (B4 — estorno sob retenção).** Uma cobrança Pix já recebida, com valor
ainda retido em escrow: `POST /payments/{id}/refund` devolve integralmente ao
pagador? O `finishReason: PAYMENT_REFUNDED` do escrow cobre exatamente esse
caso? Há prazo ou custo para esse estorno? E com split — o estorno desfaz as
pernas automaticamente?

- Resposta que aprova: estorno de primeira classe, prazo e custo conhecidos,
  desfaz o split.
- Resposta que elimina: estorno sob escrow exige intervenção manual/ticket.

**P3 (B5 — comprovante do pagador).** No comprovante Pix e no extrato bancário
do **pagador**, que nome aparece como recebedor — o nome da plataforma
(subconta-mãe), do Asaas, ou o nome civil do titular da subconta que recebeu a
perna do split? Isso vale também para a devolução (P2)?

- Resposta que aprova: pagador nunca vê o nome do recebedor da perna.
- Resposta que elimina: comprovante/extrato nomeia o titular da subconta.
  (Decisões 58/82 — inutilizável nas categorias críticas.)

## Bloco 2 — determinantes (a resposta ajusta decisões, não elimina)

**P4 (D1 — prazo máximo de retenção).** O `daysToExpire` do escrow tem teto
contratual ou de compliance? Existe retenção "até instrução" sem prazo? O que
acontece operacionalmente no vencimento (liberação automática ao recebedor —
confirmar que é isso mesmo)? O prazo pode ser estendido numa retenção já ativa?

- Consequência: com teto → decisões 89/90 (avisos + job de expiração) voltam
  com os prazos reais; sem teto → ficam arquivadas.

**P5 (D3 — taxa da plataforma).** Nossa taxa pode ser perna do split na mesma
cobrança, creditada na conta-mãe? Ela também fica sujeita ao escrow ou é
liberada de imediato? Qual o custo total: Pix de entrada + split + escrow +
eventual estorno?

**P6 (D4 — KYC do recebedor).** Para `POST /accounts` (subconta) receber perna
de split: que documentos/dados são exigidos, em que momento (criação × primeiro
recebimento × primeiro saque), e qual o prazo típico de aprovação? Um recebedor
pode ser criado **depois** da cobrança existir e ainda receber? (Nosso fluxo
cria a subconta antes da cobrança — confirmar que a ordem inversa não é
exigida.)

**P7 (D5 — MED).** Se o pagador abrir uma MED (devolução por fraude) sobre
cobrança retida ou já liberada: como a plataforma é notificada (webhook?),
que prazo tem para contestar, e quem arca quando a MED prospera sobre valor já
liberado ao recebedor?

## Bloco 3 — operacionais (entram na comparação, §3 do checklist)

- Webhooks de mudança de estado do escrow e do pagamento; política de reenvio.
- Limites de valor por transação/subconta.
- Prazo de liquidação da liberação (`finish`) até o saldo disponível do
  recebedor.
- Exigência de reserva rolante/garantia sobre a conta-mãe.

## Como registrar o resultado

1. Respostas de P1–P3: atualizar §1 do checklist. Qualquer "não" → Asaas
   eliminado, voltar à pesquisa de candidatos (e se ninguém passar no B1,
   é o achado de produto do §4 do checklist).
2. Respostas de P4–P7: registrar em §2 como fatos; abrir revisão das decisões
   89/90 conforme P4.
3. Tudo aprovado → decision-round para fechar a decisão 59 (número da vez,
   reler o log inteiro antes de numerar) e, só então, apontar o adapter para
   homologação real.
4. Divergência entre resposta e o que o adapter assume → decisão 36/37:
   emendar `api/docs/feature/payment-rail.md` e o adapter antes de qualquer
   cobrança.
