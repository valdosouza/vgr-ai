# E-mail pronto para envio ao Asaas

> Versão externa do [roteiro-perguntas-asaas.md](roteiro-perguntas-asaas.md) —
> sem numeração interna, sem decisões, sem os critérios de eliminação (esses
> ficam no roteiro, para avaliar as respostas). Enviar pelo canal comercial
> (asaas.com → "Fale com vendas") ou abrir ticket técnico; se for call, o
> roteiro interno é o guia.

---

**Assunto:** Marketplace com split + Conta Escrow — dúvidas de viabilidade
técnica antes da integração

Olá,

Estamos avaliando o Asaas como provedor de pagamentos de um marketplace e a
documentação pública já respondeu boa parte do que precisamos — em especial
sobre a Conta Escrow e o split. Antes de avançar para a integração, restam
algumas confirmações que não encontramos explícitas na documentação.

Nosso fluxo: o pagador paga por Pix; o valor deve ficar **retido na subconta
do(s) recebedor(es)** até a plataforma instruir o desfecho — liberar aos
recebedores ou devolver ao pagador. A plataforma nunca é titular do valor;
nossa taxa entraria como perna do split.

**1. Split + Conta Escrow na mesma cobrança.** Uma cobrança Pix criada com
`split` (N carteiras, valores fixos) em que os recebedores têm Conta Escrow
ativa: o valor de cada perna fica retido no escrow do respectivo recebedor até
o `finish`? Os dois produtos compõem na mesma cobrança? Há limite de
recebedores por split?

**2. Estorno com valor retido.** Uma cobrança Pix já recebida, com valor ainda
retido em escrow: o `POST /payments/{id}/refund` devolve integralmente ao
pagador? O `finishReason: PAYMENT_REFUNDED` cobre esse caso? Com split, o
estorno desfaz as pernas automaticamente? Qual o prazo e o custo?

**3. Comprovante do pagador.** No comprovante Pix e no extrato bancário do
pagador, que nome aparece como recebedor — o da plataforma (conta-mãe), o do
Asaas, ou o nome do titular da subconta que recebeu a perna do split? E na
devolução do item 2?

**4. Prazo máximo de retenção.** O `daysToExpire` do escrow tem teto
(contratual ou de compliance)? Existe modalidade de retenção "até instrução",
sem prazo? No vencimento, a liberação ao recebedor é automática? O prazo pode
ser estendido numa retenção já ativa?

**5. Taxa da plataforma.** Nossa taxa pode ser perna do split creditada na
conta-mãe, na mesma cobrança? Ela também fica sujeita ao escrow ou é liberada
de imediato? Qual o custo total do arranjo (Pix de entrada + split + escrow +
eventual estorno)?

**6. KYC das subcontas.** Para uma subconta (`POST /accounts`) receber perna de
split: que documentos são exigidos, em que momento (criação, primeiro
recebimento ou primeiro saque), e qual o prazo típico de aprovação?

**7. MED.** Se o pagador abrir uma MED sobre cobrança retida ou já liberada:
como a plataforma é notificada (webhook?), que prazo tem para contestar, e
como fica o valor já liberado ao recebedor?

Agradecemos desde já — com essas confirmações conseguimos fechar a escolha do
provedor e iniciar a integração pelo sandbox.

Atenciosamente,
Valdo
