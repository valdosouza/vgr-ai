# Plano — Identidade visual (rodada 23)

> **Rodada 23 — aberta e respondida em 2026-10-12.** Valdo: "antes da
> publicação precisamos comitar tudo que temos e abrir uma etapa de
> identidade visual, atualmente não existe". Respostas: todas na opção
> recomendada, exceto o nome, que **fica VGR** (1a, com o significado).
> Decisões **250–260** no [VGR-plano.md](../decisions/VGR-plano.md). Cada
> fase por "pode seguir" (38) — §5.
>
> **Rodada 24 — escolha da direção, 2026-10-13.** Valdo trouxe uma prancha
> própria juntando as direções da V1; respondida "1a, 2a, 3a, 4a, 5a, 6a" →
> decisões **261–266** (§7). Próxima fase: **V1b**, a direção consolidada
> na página de apresentação, por "pode seguir".

---

## 1. Origem e relação com a rodada 22

A rodada 22 deixou o caminho de implantação pronto (P1 e P2). A P3
(homologação com convidados) e a P4 (Android no teste interno) colocam o
produto na mão de pessoas, e o produto ainda não tem cara. Por isso a P3 e a
P4 **esperam esta frente**. O domínio (item 4 da rodada 22) também depende
dela: o domínio segue o nome.

Antes de abrir a frente, os três repositórios foram conferidos em
2026-10-12: nada sem commit, e os ramos de trabalho estão integrados ao
`main`/`master` (api `23e0113`, app `64799f2`, ai `44e89ac`).

## 2. O que existe hoje (verificado em 2026-10-12)

| Item | Estado |
|---|---|
| Nome no aparelho | "vgr" (Android), "Vgr" (iOS), "vgr_admin" (painel na web) |
| Ícone do app | o ícone padrão do Flutter (Android, iOS e favicon da web) |
| Cores | nenhuma: o app usa o tema padrão do Material; o manifesto web usa o azul padrão do Flutter (`#0175C2`) |
| Tipografia | nenhuma escolhida; fonte padrão do sistema |
| Tela de abertura | a padrão do Flutter |
| Modo escuro | não tratado |
| O que ajuda | a decisão 133: toda tela usa os widgets `Vgr*` do pacote `vgr_widgets`. Uma identidade aplicada ali (tokens de cor, tipo e forma) chega a todas as telas dos dois apps de uma vez. |
| Significado de "VGR" | não registrado nas decisões |

## 3. O que pesa na identidade deste produto

- **Quem usa pode estar em risco.** A rodada 21 registrou o motivo: alguém
  pode criar uma denúncia falsa para descobrir quem ajuda. Pelo mesmo
  motivo, o celular de quem denuncia pode ser visto por quem foi
  denunciado. Ícone e nome na tela inicial não devem anunciar "denúncia".
- **Confiança antes de urgência.** O produto conecta pessoas para ajudar.
  Visual de alarme (sirene, vermelho, polícia) afasta quem ajuda e chama
  atenção na tela.
- **Uso em situação difícil.** Pouca luz, mão tremendo, pressa: contraste
  alto, alvos de toque grandes e texto que aumenta sem quebrar.
- **Privacidade também na fonte.** Fonte baixada da internet em tempo de
  execução revela a terceiros que o app foi aberto (e de qual IP). A fonte
  fica dentro do app.

## 4. Pendências (rodada 23 — identidade visual)

**Respondidas em 2026-10-12**: 1a → 250 (VGR: "vigiar" lido em inglês;
Vigilância e Recompensa; Vigilant and Reward) e 251 (a identidade
representa todas as decisões); 2a → 252; 3a → 253; 4a → 254; 5a → 255;
6a → 256; 7a → 257; 8a → 258; 9a → 259; 10 → 260. O texto original das
opções fica abaixo como registro.

**1. Nome público do produto**
- (a) "VGR" continua sendo o nome público (dizer o significado, se houver).
- (b) Um nome novo trazido por você.
- (c) **Eu proponho de 6 a 8 nomes**, cada um com verificação de domínio
  `.com.br` e de conflito nas lojas, e você escolhe. *(Recomendado: o nome
  aparece no aparelho, nas lojas e no domínio, e trocá-lo depois de
  publicado custa caro.)*

**2. Discrição na tela do celular**
- (a) **Nome e ícone que não anunciam "denúncia"**: nada de sirene, distintivo
  ou olho; o app parece um app de comunidade/ajuda. Sem modo disfarce no
  MVP. *(Recomendado.)*
- (b) Além de (a), um "modo discreto" que o usuário liga para trocar ícone e
  nome por outros genéricos. Exige cuidado com as regras das lojas, que
  proíbem app que se passa por outro. Fica como visão futura com rodada
  própria se escolhida a (a).
- (c) Marca explícita, sem preocupação de discrição.

**3. Personalidade**
- (a) **Confiável e acolhedora**: serena, protetora; cores profundas e
  calmas, formas arredondadas. *(Recomendado: conversa com quem ajuda e não
  chama atenção.)*
- (b) Alerta e urgente: cores quentes e alto impacto.
- (c) Institucional e neutra, próxima de serviço público.

**4. Quem cria**
- (a) **Eu produzo 3 direções completas** (logo vetorial, paleta com
  contraste conferido, tipografia, ícone do app e 3 telas reais aplicadas)
  numa página de apresentação; você escolhe uma, refinamos, e um designer
  pode finalizar depois se quiser. *(Recomendado: rápido, barato, e a
  escolha vem de ver o produto vestido.)*
- (b) Contratar designer ou agência: eu preparo o briefing com tudo deste
  plano.
- (c) Você traz uma identidade pronta.

**5. Tipografia**
- (a) **Fonte de licença livre (OFL) embutida no app, nunca baixada em tempo
  de execução**, escolhida por legibilidade (as direções do item 4 propõem
  qual). *(Recomendado: privacidade e funcionamento sem rede.)*
- (b) Fonte do sistema de cada aparelho.

**6. Modo escuro**
- (a) **Claro e escuro desde o início, seguindo o aparelho.** *(Recomendado:
  uso à noite e tela escura chama menos atenção.)*
- (b) Só claro no MVP.

**7. Acessibilidade**
- (a) **WCAG AA como piso** (contraste 4,5:1 em texto, 3:1 em elementos
  gráficos), alvos de toque de 48 dp e texto ampliável até 200% sem
  quebrar. *(Recomendado.)*
- (b) AAA onde for possível, além do AA.

**8. Painel administrativo**
- (a) **A mesma identidade, em versão sóbria** (mesmas cores e fonte, menos
  ilustração). *(Recomendado.)*
- (b) Visual próprio, separado do app.

**9. O que a frente entrega**
- (a) **Tudo o que aparece antes da publicação**: nome no aparelho e na
  web, ícone (Android adaptativo, iOS, favicon), tela de abertura, tema
  (tokens no `vgr_widgets`, claro e escuro), painel, e o material da Play
  Store (ícone 512, imagem de destaque, capturas) que a P4 precisa.
  *(Recomendado.)*
- (b) Só ícone, nome e cores agora; o resto depois da publicação.

**10. Fatiamento (proposta)**
- **V1**: as propostas do item 4 (ou o briefing, se 4b).
- **V2**: a direção escolhida aplicada no código (tokens, ícones, tela de
  abertura, nomes), conferida no navegador nos dois apps, claro e escuro.
- **V3**: material da loja, junto com a P4.

Cada fase por "pode seguir" (38). A P3 e a P4 da rodada 22 esperam a V2.


## 5. Fases

| Fase | Conteúdo | Estado |
|---|---|---|
| **V1** | briefing a partir do log de decisões (251) + três direções completas numa página de apresentação (254): logo, paleta claro/escuro com contraste conferido (257), fonte OFL (255), ícone do app, três telas reais | **executada em 2026-10-12** — §6; escolha feita em 2026-10-13 (§7) |
| **V1b** | a direção consolidada (261–264) na página de apresentação: logo em vetor e variações, ícone, paleta clara e escura com contraste calculado, fonte, telas reais do app no claro e no escuro (266) | aguardando "pode seguir" |
| **V2** | a direção escolhida aplicada no código: tokens no `vgr_widgets`, ícones, tela de abertura, nomes, painel (258), conferida no navegador nos dois apps, claro e escuro | aguardando |
| **V3** | material da Play Store, junto com a P4 da rodada 22 | aguardando |

## 6. Execução

### V1 — 2026-10-12

- **Briefing**: [identidade-visual/briefing.md](../identidade-visual/briefing.md)
  — doze princípios, cada um com as decisões de onde vem (251).
- **Página de apresentação**: https://claude.ai/artifact/UAnfesX3oMWRfUtQfdbJFz
  (privada; fonte em `docs/identidade-visual/v1/index.html`).
- **Três direções**, cada uma com logo (símbolo + VGR + "Vigilância e
  Recompensa"), ícone (máscaras do iPhone e do Android, e numa tela inicial
  ao lado de outros apps), paleta clara e escura, fonte, três telas reais
  com os textos do app (Por perto, Denúncia, Oferecer ajuda com a caixa da
  237) no claro e no escuro, e o quadro "elemento → decisões":
  - **A · Vigília** — um arco que cobre um ponto aceso: velar por alguém.
    Azul noturno e luz âmbar. Fonte Atkinson Hyperlegible Next, feita para
    baixa visão. **Recomendada.**
  - **B · Vínculo** — duas pessoas se aproximam de uma terceira e formam o V.
    Verde-petróleo e damasco. Fonte Figtree.
  - **C · Assinatura** — o próprio nome; o G guarda um ponto dentro. Índigo
    e menta. Fonte Lexend.
- **Contraste calculado, não estimado**: dez pares por tema em cada direção
  (texto, texto secundário, botão, destaque, erro, bordas de controle,
  gráficos), todos no piso AA da 257. A conta mostrou que o tom claro do
  destaque não passa 3:1 como gráfico sobre o branco nas três direções. Por
  isso cada paleta ganhou um `accentGraphic` mais escuro para o modo claro,
  e o tom claro ficou só como fundo de texto escuro.
- **Fontes OFL reais** (Atkinson Hyperlegible Next, Figtree, Lexend): os
  logos e ícones em SVG têm as letras convertidas em contorno, então abrem
  sem a fonte instalada.
- **Arquivos** por direção em `docs/identidade-visual/v1/<direção>/`:
  `simbolo.svg`, `logo-claro.svg`, `logo-escuro.svg`, `icone.svg`. O
  gerador (`v1/gerador/`) refaz tudo a partir de `palettes.py`, que é a
  fonte dos tokens que a V2 leva para o `vgr_widgets`.
- Conferido no Chromium: as três fontes carregam e não há rolagem lateral
  em 1280 px nem em 400 px.

## 7. Escolha da direção (rodada 24, 2026-10-13)

Valdo trouxe uma prancha própria, "fiz uma junção e criei essa opção":
[v1b/prancha-valdo.webp](../identidade-visual/v1b/prancha-valdo.webp).
É a direção A (o arco com o ponto aceso, azul-marinho, dourado, Atkinson
Hyperlegible Next) com o verde-petróleo da B como cor de ação, mais o
slogan "Pessoas cuidando de pessoas. Comunidades mais seguras.", as
variações do logo e o padrão de arcos.

### Análise da prancha

**Conflitos com decisões já tomadas** (resolvidos pela 262–265):

| Na prancha | Conflito | Decisão |
|---|---|---|
| Troféu, "Você ganhou +10 pontos", aba "Recompensas" | princípio 6; recompensa opcional e nunca o motivo (1), promessa de quem denuncia a quem ajuda (30); pontos por denunciar incentivam denúncia falsa; dinheiro desligado na fase fechada (247) | 262 |
| Escudo com check | sem distintivo nem aparência policial (252; princípios 1 e 7) | 263 |
| "Olá, Ana" com foto | identidade não depende de rosto, nome ou foto (6, 40, 41); o celular pode ser visto pelo denunciado (238) | 264 |
| "Você está em uma área segura" | o app não avalia a segurança de uma área: promessa falsa e risco jurídico | 264 |
| Ponto de ônibus, cartões, garrafa, sacola | fora da frente (259); tensão com a discrição do ícone (252) | 265 |

**Contraste** (piso da 257), calculado com `v1/gerador/palettes.py`:

| Par | Medido | Mínimo | Correção (261) |
|---|---|---|---|
| dourado `#D8A34D` como gráfico sobre branco / `#F4F6F8` | 2,27 / 2,09 | 3 | `#BB8329` no claro (3,29 / 3,03); o `#D8A34D` fica como preenchimento e sobre o azul (4,82) |
| ponto dourado no ícone verde | 2,57 | 3 | sai a variação verde do ícone |
| cinza `#64748B` sobre `#F4F6F8` | 4,39 | 4,5 | `#627289` (4,52) |
| vermelho `#D64545` como texto, e texto branco sobre ele | 4,38 | 4,5 | `#D23535` (4,88) |

Passam como estão: azul-marinho sobre branco (10,93), texto branco no
verde (5,82), azul-marinho sobre o dourado (4,82), arco branco no ícone
verde (5,82).

**O que faltava**: o modo escuro (256), derivado dos escuros já conferidos
da A e da B — fundo `#0A1120`, azul `#93B6FF` (9,31), verde `#5CCDBB`
(9,79), dourado `#D8A34D` (8,32); o painel sóbrio (258); e o logo em
vetor, porque a prancha é imagem e o "VGR" dela não é a fonte escolhida.

As telas da prancha são ilustrativas. A V2 veste as telas reais do app;
"Pedir ajuda", "Informação" e a aba "Mapa" seriam funções novas, com rodada
própria.

### Respostas

1a → 261 (a composição é a direção, com contraste corrigido, escuro
derivado e logo em vetor); 2a → 262 (sem troféu e sem pontos); 3a → 263
(o arco substitui o escudo); 4a → 264 (sem foto, nome ou "área segura" na
tela inicial); 5a → 265 (aplicações fora do app em rodada futura); 6a →
266 (V1b antes da V2).
