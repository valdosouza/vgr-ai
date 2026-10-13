# Plano — Site do VGR (rodada 25)

> **Rodada 25 — aberta e respondida em 2026-10-13** ("1a, 2a, 3a, 4a, 5a,
> 7a, 8a, 9a, 10 ok") → decisões **267–275** no
> [VGR-plano.md](../decisions/VGR-plano.md). **Em aberto: item 6** (quem
> responde pelos dados); os textos levam campos marcados até lá.
>
> Valdo: "antes vamos criar um
> website multi-language português e inglês para que todos possam ter todas
> as informações sobre o aplicativo, assim podemos publicar o site, o
> backend, o aplicativo e o painel admin". O site entra antes da produção.
> As perguntas de produção propostas no mesmo dia passam a ser a rodada 26
> ([plano-producao.md](plano-producao.md) §5). Cada fase por "pode seguir"
> (38) — §5.

---

## 1. Origem

A identidade visual (rodadas 23 e 24) terminou com a V2 integrada nos dois
apps. O próximo passo era a P3 (homologação no servidor). Antes dela, Valdo
pediu um site em português e inglês, publicado junto com a API, o app e o
painel: o lugar onde qualquer pessoa entende o que é o VGR.

## 2. O que existe hoje (verificado em 2026-10-13)

| Item | Estado |
|---|---|
| Site | não existe |
| Termos de uso | **não existem**, mas o cadastro do app já pede "Concordo com os termos de uso" (`auth.register.consent`), sem link para texto nenhum |
| Política de privacidade | não existe; a 244 já diz que "o aviso de privacidade" informa os 30 dias de backup |
| Exclusão de conta pelo titular | **não existe**: a API só apaga usuários da equipe pelo painel (`DELETE /users/:id`). O Google Play exige, para app com cadastro, exclusão de conta dentro do app **e** um endereço na web para pedi-la; a LGPD (art. 18) dá ao titular o direito de pedir a eliminação |
| Contato público | não existe |
| Identidade | pronta: cores, fonte, símbolo e logo (`identidade-visual/v1b/`) |
| Domínio | em aberto (item 4 da rodada 22) |

## 3. O que pesa no site

- **Informar e proteger ao mesmo tempo.** O site explica que o app serve
  para denunciar e para ajudar, e a loja exige que a descrição diga o que o
  app faz. Ao mesmo tempo, o ícone e o nome no celular seguem discretos
  (252), e o tom é o da identidade: "Pessoas cuidando de pessoas", sem
  sirene, polícia ou crime em imagem (253).
- **Privacidade também no site.** Quem visita um site sobre denúncia pode
  estar em risco. Nada de cookies, rastreador, fonte ou script de terceiros
  (a mesma razão da 255), e nenhum formulário que guarde dados.
- **O que a loja e a LGPD pedem.** Política de privacidade (endereço
  obrigatório no Play Console), página de exclusão de conta, contato de
  suporte e o encarregado de dados.
- **Fase fechada (247).** Até a revisão jurídica (228), o app roda com
  convidados e sem recompensa em dinheiro. O site não pode prometer o que
  ainda não está ligado.
- **Acessível (257).** WCAG AA, claro e escuro, texto ampliável, funciona
  sem JavaScript.

## 4. Pendências (rodada 25 — site)

**Respondidas em 2026-10-13**: 1a → 267; 2a → 268; 3a → 269; 4a → 270;
5a → 271; 7a → 272; 8a → 273; 9a → 274; 10 → 275. **Em aberto: 6.** O
texto original das opções fica abaixo como registro.

**1. Conteúdo**
- (a) **Início · Como funciona** (denunciar; as cinco formas de ajudar;
  recompensa opcional; pânico) **· Segurança e privacidade** (anonimato
  como padrão, o que fica guardado e por quanto tempo) **· Perguntas
  frequentes · Baixar o app · Contato · Termos de uso · Política de
  privacidade · Excluir conta e dados.** Contato por e-mail exibido como
  texto (`contato@` e `privacidade@` no domínio), sem formulário.
  *(Recomendado: cobre o que as pessoas perguntam e o que a loja e a LGPD
  exigem.)*
- (b) Só a página inicial e as páginas legais.

**2. Idiomas**
- (a) **Português e inglês em endereços próprios (`/pt/` e `/en/`), com
  seletor em toda página; a primeira visita vai para a língua do
  navegador. O texto em português é o que vale juridicamente; o inglês é
  tradução.** *(Recomendado.)*
- (b) Os dois idiomas na mesma página.

**3. Como o site fala de "denúncia"**
- (a) **Diz com clareza o que o app faz** — avisar que algo está
  acontecendo e receber ajuda de quem está perto —, no tom da identidade,
  sem imagem de crime, polícia ou sirene. O ícone no celular continua
  discreto. *(Recomendado: a loja exige a descrição real, e as pessoas
  confiam no que entendem.)*
- (b) Linguagem genérica ("ajuda entre vizinhos"), sem a palavra
  "denúncia" em destaque.

**4. Disponibilidade durante a fase fechada (247)**
- (a) **"Em testes com convidados"**, com o e-mail de contato para quem
  quiser participar; sem lista de espera no site. *(Recomendado: o site não
  guarda dado de ninguém.)*
- (b) Lista de espera com formulário (exige guardar e-mails, com aviso e
  consentimento).
- (c) O site só vai ao ar na abertura ao público.

**5. Termos de uso e política de privacidade**
- (a) **Eu redijo a partir das decisões** (o que é guardado e por quanto
  tempo, anonimato e responsabilização (23), backup de 30 dias (244), logs
  de 14 dias (245), recompensa como promessa (30), Legal Gate (104),
  pânico), marcados como versão para revisão jurídica e entregues à revisão
  da 228 antes da abertura ao público. Na fase fechada valem como aviso aos
  convidados. *(Recomendado: os convidados precisam de um texto antes de
  usar, e o app já pede o aceite.)*
- (b) Um advogado escreve; o site espera por ele.

**6. Quem responde pelos dados (LGPD)** — informar: razão social, CNPJ,
endereço e o e-mail do encarregado de dados (pode ser você). Entram na
política de privacidade e no rodapé.

**7. Exclusão de conta**
- (a) **Rodada própria logo depois do site** para a exclusão de conta
  pelo app (o que some, o que fica pelo prazo de responsabilização da 23, e
  os 30 dias de backup da 244). Enquanto isso, o site publica a página
  "Excluir conta e dados" com o pedido por e-mail para `privacidade@`.
  O app passa a ligar o aceite do cadastro aos termos publicados.
  *(Recomendado: a P4 depende disso, e apagar dado esbarra na
  responsabilização, que pede decisão.)*
- (b) Só o pedido por e-mail, atendido à mão pelo painel.

**8. Como o site é feito**
- (a) **Repositório novo `vgr-site`**: site estático gerado a partir de um
  texto por idioma, com a mesma identidade (cores, fonte embutida,
  símbolo), claro e escuro; sem cookies, sem rastreador, sem fonte ou
  script de terceiros, funcionando sem JavaScript. *(Recomendado.)*
- (b) Uma pasta dentro do vgr-app.
- (c) Construtor de sites de terceiros (WordPress, Wix…).

**9. Onde fica**
- (a) **No mesmo servidor (240)**, servido pelo Caddy em `<domínio>` e
  `www.<domínio>`, publicado junto com a API, o app e o painel na P3.
  Nenhuma métrica de visita além da contagem dos logs do servidor (14 dias,
  245). *(Recomendado: nenhum terceiro vê quem visita.)*
- (b) Hospedagem estática gratuita (GitHub Pages, Cloudflare Pages) já
  agora; o provedor vê os acessos.

**10. Fatiamento (proposta)**
- **S1**: os textos em português e inglês (incluindo termos e política)
  numa página de revisão, para você aprovar.
- **S2**: o site construído no `vgr-site`, conferido no navegador (claro e
  escuro, português e inglês, celular e computador).
- **S3**: publicação junto com a P3 (Caddy e `DEPLOY.md`).

## 5. Fases

| Fase | Conteúdo | Estado |
|---|---|---|
| **S1** | textos pt/en, inclusive termos e política, numa página de revisão | **executada em 2026-10-13** — §6; aguardando a aprovação de Valdo |
| **S2** | site estático no `vgr-site`, conferido no navegador | aguardando |
| **S3** | publicação com a P3 | aguardando |

## 6. Execução

### S1 — 2026-10-13

Por "pode seguir" de Valdo.

- **Levantamento antes de escrever**: um agente leu o log de decisões
  inteiro, o resumo, os planos e conferiu no código da API e do app o que
  cada função faz de verdade (o que é guardado, quem vê, por quanto tempo,
  o que está ligado, desligado na fase fechada ou só decidido). Os textos
  descrevem só o que o sistema faz hoje.
- **Textos** em `docs/site/textos/{pt,en}/`, um arquivo Markdown por página
  (cabeçalho YAML), as nove páginas da 267. Cada parágrafo cita as
  decisões de onde vem; o que é proposta de Claude, e não decisão (bases
  legais da LGPD, foro, prazo de resposta, parte das regras de uso), vai
  marcado como proposta para a revisão jurídica. Cerca de 5.500 palavras
  em português; o inglês é tradução (268).
- **Página de revisão**: https://claude.ai/artifact/FK25iVCpg2gmYYx867DMvR
  (privada; gerada por `docs/site/revisao/build.py`), com as páginas em
  português e inglês lado a lado, as decisões de cada parágrafo, os campos
  que faltam e os pontos abaixo.
- **Campos que faltam**: razão social, CNPJ, endereço e encarregado (item
  6), domínio (rodada 26), data de vigência, idade mínima, provedores do
  servidor, do backup e do e-mail, parceiro de pagamento, e os prazos de
  guarda ainda sem decisão.

**Pontos para decidir e para a revisão jurídica**, achados na redação:

- **Idade mínima**: não há decisão.
- **Prazos de guarda sem decisão**: conta, ofertas de ajuda, avaliações,
  indicações de direção, alertas de pânico, registro oculto e auditoria.
  Vão para a rodada da exclusão de conta (272).
- **Marco Civil da Internet, art. 15**: o provedor de aplicação deve
  guardar registros de acesso (IP, data e hora) por 6 meses; hoje os
  registros técnicos duram 14 dias (245) e a API não registra IP (110).
- **Propostas, não decisões**: bases legais, foro, prazo de resposta de 15
  dias e as regras de uso marcadas.

**Divergências entre o app e as decisões**, achadas no levantamento (o
site não promete nada disso; pedem correção em rodada própria):

- o app diz que o pânico avisa os Respondentes "próximos"; o sistema avisa
  todos os aprovados, sem filtro de distância;
- o app diz que confirmar o e-mail é "necessário só para oferecer ou
  receber recompensa"; a exigência (123, 151) não está ligada;
- uma conta que denunciou anonimamente consegue oferecer recompensa pela
  API (33 diz que não);
- não existem no app a recuperação de senha, o aviso de denúncia falsa
  antes de denunciar (57) e a guarda da sessão no armazenamento seguro do
  celular (117);
- também registrado no levantamento: no risco alto a linha do tempo ainda
  mostra o horário exato de cada oferta ao dono e aos participantes (41,
  em parte); as mensagens do chat ficam em texto no banco, sem cifra.
