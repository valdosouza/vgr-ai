# Plano — Site do VGR (rodada 25)

> **Rodada 25 — aberta em 2026-10-13.** Valdo: "antes vamos criar um
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
| **S1** | textos pt/en, inclusive termos e política, numa página de revisão | aguardando a rodada 25 |
| **S2** | site estático no `vgr-site`, conferido no navegador | aguardando |
| **S3** | publicação com a P3 | aguardando |
