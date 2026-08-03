# Checklist de requisitos do PSP — fecha a pendência da decisão 59

> O que perguntar a cada PSP candidato (Mercado Pago, Pagar.me, Asaas, Iugu, …)
> antes de comparar preço. Cada item nasce de uma decisão registrada; um "não"
> nos itens **bloqueantes** elimina o fornecedor, não abre negociação.
>
> Data: 2026-08-03 · Status: pronto para uso · Decisões 30, 39, 58, 81, 82, 84,
> 85, 88, 91, 92, 95, 96, 98, 100, 102

---

## O fluxo, em uma frase (decisão 100)

O denunciante paga por Pix; **o PSP retém o valor**; o VGR **instrui o desfecho**
— caso encerrado, paga o(s) helper(s) ou devolve ao denunciante. O VGR nunca
recebe, nunca segura, nunca movimenta.

## 1. Bloqueantes — um "não" elimina o fornecedor

| # | Pergunta | Por que é bloqueante |
|---|---|---|
| B1 | **Em nome de quem fica o valor retido?** Conta do próprio PSP, do recebedor, ou subconta titularizada pelo marketplace? | Decisão 84 (custódia zero). "Titularizada pelo marketplace" torna o VGR titular de dinheiro de terceiro, derruba a isenção da decisão 81 e traz a Lei 12.865/2013 de volta. Depois da decisão 95 não há mecanismo alternativo — este item sozinho decide se o produto tem selo de reserva. |
| B2 | **Pix com retenção existe?** Recebimento via Pix cujo valor fique retido até instrução da plataforma. | É o mecanismo único que sobrou (decisões 95, 100). |
| B3 | **A liberação aceita N recebedores numa mesma instrução?** | Decisão 30(c): recompensa dividida entre helpers que cumprem a condição simultaneamente. Split de um recebedor só não atende. |
| B4 | **A devolução ao pagador é operação de primeira classe**, com prazo e custo conhecidos? | Decisões 92 e 100: denúncia não resolvida devolve. Não pode ser exceção manual. |
| B5 | **O comprovante/extrato do PAGADOR nomeia o recebedor?** | Decisões 58 e 82: o denunciante não pode descobrir quem é o helper. Um PSP cujo comprovante exiba o recebedor é inutilizável nas categorias críticas — que são as que mais dependem do mecanismo. |

## 2. Determinantes — a resposta muda decisões já tomadas

| # | Pergunta | O que ela decide |
|---|---|---|
| D1 | **Há prazo máximo de retenção?** Qual? | Item 17 da rodada 3. Se houver, o vencimento volta a existir e as decisões 89 (avisos de expiração) e 90 (job agendado) se aplicam com prazos novos; se não houver, ambas podem ser arquivadas. |
| D2 | **Dá para consultar o estado vivo da reserva** por API/webhook? | Decisão 85: o selo exibido deriva da reserva viva, nunca de um booleano gravado na oferta. Sem consulta, o selo não pode ser honesto. |
| D3 | **A taxa da plataforma sai como perna do split**, na mesma instrução? | Decisão 39 + 84: a taxa não pode ser retenção de dinheiro que o VGR tenha segurado. |
| D4 | **Que KYC é exigido do recebedor**, e em que momento? | Decisão 60: a identificação do helper existe no plano administrativo e o KYC do PSP é compatível com isso — mas o momento importa, porque KYC no meio do fluxo trava o pagamento de quem já ajudou. |
| D5 | **Devolução por MED**: como chega, que prazo de resposta o facilitador tem? | Decisão 102: é o único caminho de "chargeback" que sobra no Pix. Define quanto tempo o VGR tem para contestar com a prova da decisão 92. |
| D6 | **Sandbox e ambiente de homologação** disponíveis? | Decisão 79: desenvolvimento e demonstração não podem depender de mover dinheiro real. |

## 3. Operacionais — não eliminam, mas entram na comparação

- Custo por transação de entrada (Pix), por liberação e por devolução — a taxa
  da decisão 39 precisa caber acima disso.
- Prazo de liquidação da liberação ao helper (a decisão 94 esvaziou a espera por
  contestação, mas o prazo operacional do PSP continua existindo).
- Webhooks de mudança de estado, e se há reenvio em caso de falha.
- Limites de valor por transação e por conta.
- Exigência de reserva rolante sobre os recebíveis do VGR (não fere a
  decisão 84 — é dinheiro do próprio VGR — mas prende caixa).
- Suporte a mais de um país, ainda que a decisão 96 já tenha optado por um
  adapter por jurisdição.

## 4. Como usar o resultado

1. Elimine quem falhar em qualquer item de §1.
2. Registre as respostas de §2 como **fatos**, não decisões — e abra a revisão
   das decisões 89/90 conforme D1.
3. O fornecedor escolhido fecha a pendência da **decisão 59** e vira uma decisão
   nova, com o número da vez.
4. Se **nenhum** candidato passar em B1, isso é achado de produto, não de
   compras: significa escolher entre não ter selo de reserva e revisar a
   decisão 84 — e essa escolha volta para o log de decisões, não para a
   negociação.
