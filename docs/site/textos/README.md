# Textos do site (rodada 25, S1)

Fonte dos textos do site do VGR, um arquivo por página e por idioma
(decisões 267–275). A S2 gera o site a partir daqui.

- `pt/` é o texto que vale juridicamente (268); `en/` é a tradução, com os
  mesmos arquivos na mesma ordem.
- Cada arquivo começa com um cabeçalho YAML (`title`, `description`,
  `slug`, `order`, `legal`) e segue em Markdown: `##`/`###`, parágrafos,
  listas com `-`, **negrito** e [links](/pt/contato/).
- `<!-- 23, 244 -->` ao fim de um parágrafo ou item cita as decisões de onde
  ele vem. Não aparece no site; a página de revisão mostra.
- `[[CAMPO]]` marca o que ainda falta: os dados de quem responde pelos
  dados (item 6 da rodada 25), o domínio (rodada 26) e a data de vigência.

A página de revisão: `../revisao/build.py` → `../revisao/index.html`.
