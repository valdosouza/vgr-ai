# Prompt — Fase 0: Conceito do App VGR

## Contexto

A intenção é criar um aplicativo cujo propósito central é gerar um **vínculo entre
duas ou mais pessoas**, para que elas se ajudem mutuamente. O vínculo pode ser:
- Um para um (1:1)
- Um para dois (1:2)
- Dois para um (2:1)
- Vários ao mesmo tempo (N:N)

O gatilho inicial do vínculo é **denunciar algo que está acontecendo**. A partir
dessa denúncia, outras pessoas interessadas se conectam para ajudar a resolver o
problema relatado. Recompensa (decisão 1) é um mecanismo flexível e opcional, não
o núcleo obrigatório do produto.

## Objetivos (numerados)

1. Permitir que uma pessoa registre uma denúncia/ocorrência de algo que está
   acontecendo.
2. Conectar essa denúncia a uma ou mais pessoas interessadas em ajudar,
   priorizando proximidade geográfica (decisão 2).
3. Viabilizar que essa ajuda resolva (ou avance a resolução d)o problema
   relatado, com o helper escolhendo como quer ajudar (decisão 5).
4. Suportar relações de ajuda em múltiplas configurações: 1:1, 1:2, 2:1, N:N.
5. Suportar diferentes níveis de identidade/registro por papel (denunciante,
   helper anônimo, helper identificado, policial) — decisão 4.
6. Proteger denunciantes e helpers contra retaliação (decisão 6).

## Fluxo (workflow)

```
[Pessoa A] --denuncia algo (categoria + objeto/sujeito)--> [Sistema]
                                                                |
                                                                v
                              [Sistema calcula raio dinâmico por tipo de caso]
                              [Sistema ordena por proximidade + mais recentes]
                                                                |
                                                                v
        [Pessoa(s) B, C, ...] --escolhem tipo de ajuda--> [Problema]
                                                                |
                                                                v
                              [Recompensa opcional, conforme combinado]
```

## Especificações agrupadas por domínio

### Denúncia / Ocorrência — taxonomia (decisão 3)

Sem limitação de tipos — qualquer denúncia é importante para quem denunciou. A
taxonomia do app anterior foi analisada (nomes dos arquivos em
`D:\ProjetoVGR\docs\categoria` e `D:\ProjetoVGR\docs\Objetos`) e revela um
modelo de **dois eixos**, usado como semente inicial (não como limite fechado):

**Eixo 1 — Categoria (natureza do incidente)**: agressão, ambiental, assalto,
assassinato, comércio ilegal, desaparecido, foragido, sequestro, suspeito,
tráfico, trânsito, vandalismo.

**Eixo 2 — Objeto/sujeito envolvido (quem ou o que está no centro da
denúncia)**:
- Pessoas: adulto, criança, idoso, deficiente, homem, mulher, casal, dupla,
  cidadão, pessoas (grupo), público
- Itens/situações: armas, cadáver, comércio, contrabando, drogas, combustível,
  remédio, veículo
- Ambiental: corte de árvore, desmatamento, resíduos em rios
- Contexto: estacionamento, residência, velocidade, ultrapassagem
- Outros: pets/animais, outros

Ver pendência 9 sobre como essa taxonomia deve evoluir (curada vs. livre).

### Conexão entre pessoas (decisão 2)
- Critério primário: **proximidade geográfica** — usuário vê o que está
  acontecendo perto dele.
- Ordenação padrão: mais recentes primeiro (ação rápida e efetiva).
- Refinamento secundário (quando o volume de denúncias próximas é alto):
  filtro por categoria ou escolha manual.

### Raio de atuação (decisão 7)
Dinâmico, em km, calculado a partir da localização atual do usuário — não é um
valor fixo. Varia por tipo de caso:

| Tipo de caso | Comportamento do raio |
|---|---|
| Animal perdido | Grande, pode crescer muito (achados a longas distâncias) |
| Roubo de veículo | Cresce com tempo decorrido × velocidade média |
| Violência doméstica | Pequeno (tipicamente vizinhança) |
| Violência pública | Depende da localização/coragem de quem testemunhou |
| Roubo a loja/celular | Proximidade (raio pequeno) |

**Visão de funcionalidade avançada (ainda não decidida como MVP — ver
pendência 11):** previsão de trajetória a partir de apontamentos acumulados
(ex.: cão já percorreu 10km em determinada direção → prever área provável nas
próximas horas → notificação push proativa para usuários dessa área: "Cachorro
perdido nas tuas proximidades, ajude..."). Aplicável a sequestros, roubo de
veículo, animais perdidos — cada categoria com um modelo de velocidade
diferente (pessoa a pé, veículo, animal).

### Recompensa (decisão 1)
Flexível e opcional — não necessariamente financeira. Pode ser: dinheiro,
vantagens/benefícios (ex: desconto de comerciante), reciprocidade/confiança
(favor de vizinhança), ou nenhuma retribuição. Depende do contexto da
denúncia; a maioria dos usuários tende a ajudar por recompensa, mas isso varia
caso a caso (ex.: amantes de animais ajudam a procurar cão perdido só por
empatia).

Casos de referência documentados pelo dono do produto:
1. Cão perdido → recompensa opcional; parte dos usuários ajuda só por empatia.
2. Criança desaparecida → normalmente sem dinheiro envolvido; requer pesquisa
   jurídica (pendência 8).
3. "Fiquem de olho na minha casa enquanto viajo" → favor de vizinhança,
   recompensa implícita = confiança/reciprocidade.
4. Comerciante oferece dinheiro/vantagens a quem informa situações suspeitas
   nas proximidades do comércio.
5. Roubo de veículo → apontamento coletivo de direção pela comunidade (raio
   calculado por tempo × velocidade média); **cuidado de design**: agregar o
   maior número de apontamentos antes de expor a direção, para evitar que o
   ladrão faça engenharia reversa e descubra que está sendo rastreado.
6. Policiais em atividade podem ter acesso a essa informação (ver decisão 4).

### Identidade e cadastro (decisão 4)
Modelo em camadas, por papel:
- **Anônimo**: permitido — para quem quer ajudar mantendo distância/sem
  aparecer no início. Risco: pessoas mal-intencionadas tentando atrapalhar
  investigação.
- **Denunciante**: cadastro um pouco mais elaborado; sujeito a regras
  LGPD/GDPR por país (pendência 8).
- **Helper**: pode ser anônimo ou identificado, por escolha própria — mas se
  quiser recompensa, cadastro se torna obrigatório (responsabilização,
  LGPD/GDPR).
- **Policial**: categoria possível, com processo de validação — nunca
  aprovação imediata (pendência 12). Não impede que um policial use o app
  como cidadão comum, sem essa categoria.

### Tipo de ajuda (decisão 5)
Sem definição fixa/objetiva — não se sabe a competência de cada helper de
antemão. O app deve oferecer **opções de tipo de ajuda** para o helper
escolher como quer contribuir (pendência 10 define as opções iniciais).

### Identificação entre as partes (decisão 6)
Escolha de cada helper, três modos possíveis:
- (a) ajudar sem querer nada em troca
- (b) ajudar e querer receber algo
- (c) ajudar mas não querer ser identificado

**Requisito de design explícito**: proteção contra retaliação. A maioria das
pessoas não se envolve por medo de retaliação — o app deve proteger essas
pessoas.

## Entregáveis

| Item | O que faz | Quando |
|---|---|---|
| Este documento | Registra o conceito e as decisões | Fase 0 (em andamento) |
| `docs/specs/{domain}/` | Especificação DDD completa (via skill `scope-refinement`) | Depois que a rodada 2 fechar |

## Decisões registradas

1. **Recompensa é flexível e opcional, não necessariamente financeira**;
   depende do contexto da denúncia. Ver seção "Recompensa" acima para os 6
   casos de referência.
2. **Conexão entre pessoas é baseada primariamente em proximidade
   geográfica**, ordenada por mais recentes; categoria/manual como
   refinamento secundário.
3. **Sem limitação de tipos de denúncia.** Taxonomia antiga
   (categoria × objeto/sujeito) usada como semente inicial, não como limite
   fechado.
4. **Modelo de identidade em camadas por papel**: anônimo, denunciante,
   helper (anônimo ou identificado), policial (com validação).
5. **"Ajudar a resolver" não tem definição fixa** — o helper escolhe entre
   opções de tipo de ajuda oferecidas pelo app.
6. **Identificação entre denunciante e helper é escolha do helper**, com
   proteção contra retaliação como requisito explícito de design.
7. **Raio de atuação é dinâmico em km**, calculado pela localização atual do
   usuário, variando por tipo de caso (ver tabela "Raio de atuação").
8. **Pesquisa jurídica de recompensa/casos sensíveis focada em LGPD/Brasil
   para o MVP.** Modelo de dados já preparado para regras por país (campo de
   jurisdição), mas regras de outros países não são implementadas agora.
9. **Taxonomia evolui em modelo híbrido**: lista curada (categoria × objeto,
   semente do app anterior) + campo livre de tags, para não perder a
   promessa de "sem limitação" e ao mesmo tempo evitar denúncias mal
   categorizadas/spam.
10. **Opções iniciais de "tipo de ajuda"** que o helper escolhe ao se
    candidatar a uma denúncia: presença física no local, repassar informação
    a autoridades, apoio remoto/orientação, divulgar/compartilhar para
    aumentar alcance, contribuição financeira.
11. **Previsão de trajetória + notificação push proativa fica documentada
    como visão, fora do MVP.** O MVP usa raio dinâmico simples (decisão 7),
    sem modelo preditivo de velocidade/direção.
12. **Validação de cadastro policial fica fora do MVP.** No MVP, policial
    usa o app como cidadão comum (sem categoria especial); "policial
    validado" é fase futura.
13. **Stack mobile: Flutter.** Um código-base para Android e iOS, Dart.
14. **Localização do projeto: `D:\ProjetoVGR\app`.** Pasta separada de
    `AI/` (kits) e `docs/` (planejamento/decisões).
15. **App e API seguem a MESMA estrutura do setes-app/setes-api**
    (`D:\Gestao2027`): Clean Architecture com módulos simétricos entre
    cliente e servidor. App: Flutter workspace (`flutter_modular` + `bloc` +
    `dartz Either<Failure,T>`), packages `core`/`vgr_widgets`/
    `vgr_validators` PRÓPRIOS do VGR (não reaproveita os pacotes do
    setes-app, para não acoplar o ciclo de release). API: Express/TypeScript
    modular (`interface/dto/repository/service/controller/routes` por
    módulo), MySQL com padrão `tb_` + soft delete.
16. **API é um projeto novo e independente**: `D:\ProjetoVGR\api`
    (`vgr-api`), banco e ciclo de deploy próprios — não entra como módulos
    dentro do `setes-api` existente.
17. **Padrão internacional: código, comentários e documentação técnica
    (ARCHITECTURE.md, TESTS.md, mensagens de erro da API) em inglês.** App
    já preparado para internacionalização desde a decisão 15
    (`easy_localization`, com inglês como idioma-fonte). Este documento
    (`VGR-plano.md`, registro de decisões de negócio em português) e os
    demais documentos em `docs/decisions/` ficam de fora — são o registro
    da conversa com o dono do produto, não parte do software entregável.

    ⚠️ **Nova pendência**: mensagens de erro retornadas pela API devem ser
    multi-idioma (i18n de verdade) ou só em inglês no MVP, com tradução
    ficando por conta do app? Assumido por padrão: inglês fixo no MVP,
    i18n de erros de API fica para fase futura — a confirmar.

18. **Report resolvido mantém Help Offers vinculados.** Ao resolver, todos
    os helpers vinculados continuam ligados ao report e recebem uma
    mensagem de agradecimento/fechamento — não são removidos/desvinculados.
19. **Report editado/retirado mantém helpers vinculados**, com notificação
    de que o report foi editado (podendo manter interesse) ou resolvido
    (agradecimento/fechamento). As interações do report (edições,
    resolução) formam uma timeline de eventos.
20. **Anti-fraude de papel**: a mesma pessoa não pode ser denunciante E
    helper do mesmo report simultaneamente. O denunciante pode interagir
    com o próprio report (timeline), mas não se registra como helper nele.
21. **NearbyReportsFeed é paginado**, com ordenação por mais recente ou por
    relevância.
22. **Apontamento de direção (Direction Sighting) processa de forma
    síncrona** — prioridade é agilidade da informação, não processamento
    em lote.
23. **Responsabilização de anônimos**: IP e outras informações não-ilegais
    de coletar são sempre registrados internamente, mesmo para
    denunciante/helper "anônimo" — o anonimato é social/de interface, não
    forense.
24. **Jurisdição**: aplica-se sempre a lei brasileira (LGPD),
    independente da localização física do usuário — sem geo-bloqueio ou
    lógica adaptativa de jurisdição no MVP.
25. **Retenção de dados de menores/criança desaparecida: até 90 dias após
    a resolução do Report, com exclusão automática depois disso.** Base
    legal preliminar: art. 14 LGPD (melhor interesse da criança) + art. 7
    LGPD (proteção da vida/incolumidade física, dispensa consentimento em
    emergência). ⚠️ Pesquisa preliminar, não é parecer jurídico formal —
    confirmar com advogado antes do lançamento, mas não bloqueia o MVP.
26. **Reconciliação de Direction Sighting**: modelo estatístico
    ponderado — estimativa inicial 50/50 (ex. norte/sul) até que mais
    apontamentos desloquem a probabilidade; não é voto majoritário simples.
27. **Mitigação anti-fraude nos apontamentos**: apontamento de helper
    anônimo tem peso menor que o de helper identificado na agregação
    estatística — mitigação, não solução completa.
28. **Fila offline obrigatória**: denúncias/apontamentos são gravados
    localmente quando sem internet e disparados conforme conectividade/
    disponibilidade do servidor — também serve como controle de fluxo em
    picos de tráfego.
29. **Raio dinâmico pertence ao domínio "Help Matching"**, não ao domínio
    "Report Management".
30. **Recompensa é modelada como "Promessa de Recompensa" (Código Civil,
    arts. 854-860)** — instituto jurídico brasileiro específico para este
    caso. Regras incorporadas ao design: (a) a promessa obriga o
    denunciante assim que a condição é cumprida, mesmo que o helper não
    tenha agido pela recompensa; (b) revogação só é válida se publicada da
    mesma forma que a oferta original **e antes** de alguém cumprir a
    condição — denunciante não pode cancelar após a recompensa já ter sido
    "ganha"; (c) se dois ou mais helpers cumprem a condição
    simultaneamente, a recompensa é **dividida automaticamente** entre
    eles por padrão (fallback de decisão 30 quando o denunciante não
    escolhe um único helper). ⚠️ Pesquisa preliminar — confirmar com
    advogado antes do lançamento, mas não bloqueia o MVP.
31. **Login: Google, Apple, Facebook + telefone/WhatsApp OTP como 4º
    método confirmado.** Os quatro métodos fecham a estratégia de login
    social/frictionless (decisão 31 fechada).
32. **Anonimato do denunciante é uma escolha explícita e independente**,
    justificada por: risco iminente, ou envolvimento próximo com a
    situação denunciada (risco de retaliação). Trade-off aceito: anonimato
    aumenta o risco de fraude/trote — mitigado pelo log oculto de
    responsabilização (decisão 23), não pelo bloqueio do anonimato.
33. **Denunciante precisa estar registrado (não-anônimo) para oferecer
    recompensa** — responsabilização pelo pagamento da recompensa exige
    identidade. Denúncia sem recompensa continua podendo ser 100%
    anônima (decisão 32). Isso refina a decisão 4/30: anonimato do
    denunciante e oferta de recompensa são mutuamente exclusivos.
34. **Elegibilidade de recompensa do helper exige registro** (confirma a
    decisão 4), mas **helpers anônimos continuam podendo participar** de
    denúncias com recompensa — o denunciante pode explicitamente permitir
    que anônimos ajudem voluntariamente. O helper anônimo deve ser
    informado, antes de ajudar, que não poderá reivindicar a recompensa.
35. **Sem recompensa envolvida, ajuda anônima é aceita integralmente**,
    sem exigência de registro de nenhum dos lados.
36. **Governança SDD (Spec-Driven Development) — regra 1: specs são
    sempre vinculantes.** Auditoria do harness (`vgr-kit`) encontrou que
    `tdd-orchestrator` só trata `docs/specs/{domain}/003-*-tactical-design.md`
    e `004-*-test-scenarios.md` como obrigatórios em modo autônomo — em
    modo interativo a própria skill cai para "analisar o requisito"
    livremente. Para o VGR: **as specs são sempre vinculantes**,
    independente do modo, em qualquer implementação de tarefa.
37. **Governança SDD — regra 2: emenda antes de divergir.** Nenhuma skill
    do harness é autorizada a atualizar `docs/specs/` após a
    implementação (`project-memory` é explicitamente proibida de tocar
    nessa pasta; só `scope-refinement` pode escrever lá, e nada o
    rechama automaticamente). Regra do projeto: **se o código revelar que
    a tactical design ou os cenários de teste estavam incompletos/errados,
    parar a implementação, emendar o documento de spec com uma nota
    "Amended — Task NN: o que mudou e por quê" (espelhando o "REVISED by
    decision N" deste documento), e só então retomar o código.** Nunca
    deixar spec e código divergirem silenciosamente.
38. **Modo de execução do backlog: interativo, tarefa por tarefa** — não
    o `autonomous-orchestrator` hands-off. Escolhido pela sensibilidade
    das decisões envolvidas (LGPD, recompensa) exigir revisão contínua do
    dono do produto. Pode ser revisto depois, uma vez que o time e o
    domínio estejam mais maduros.

## Monetização e segurança contra uso malicioso da recompensa

39. **Monetização combinada, sem anúncios**: doações (individuais +
    institucionais/B2G — prefeituras, ONGs, empresas locais patrocinando a
    operação na região) + taxa de intermediação sobre recompensas em
    categorias não-sensíveis (a intermediação de pagamento já é
    obrigatória pela decisão 30, cobrar uma taxa nela é a monetização mais
    natural). Anúncios descartados: conflito de imagem em conteúdo
    sensível (denúncia ao lado de anúncio) e conflito direto com as
    decisões de anonimato (6, 23, 32), que dependem de não rastrear o
    usuário. ⚠️ **Nova pendência**: intermediar pagamento de terceiros
    pode exigir registro como instituição de pagamento perante o Banco
    Central (Lei 12.865/2013) — pesquisa jurídica pendente, mesmo padrão
    das decisões 25/30.
40. **Categorias têm um nível de risco (RiskTier) que restringe as regras
    de identificação do helper — não é mais uma escolha totalmente livre
    do helper (decisão 6) em todos os casos.** Para categorias de
    altíssimo risco de retaliação por crime organizado (tráfico,
    sequestro, e desaparecimento de criança quando há suspeita de
    organização criminosa envolvida), **a identificação do helper é
    proibida**, mesmo que ele queira se identificar ou queira a
    recompensa. Para as demais categorias, a decisão 6 continua valendo
    sem alteração.
41. **Sinais de engajamento em tempo real ficam ocultos do denunciante
    para as mesmas categorias de altíssimo risco da decisão 40** —
    contagem e timestamp de Help Offers não são mostrados em tempo real,
    para quebrar a correlação temporal que um agente malicioso (ex:
    traficante se passando por denunciante) poderia usar pra inferir
    identidade de quem respondeu à denúncia.
42. ⚠️ **Nova pendência**: se identificação é proibida nas categorias da
    decisão 40, como um helper anônimo recebe uma recompensa monetária
    sem se identificar? Sugestão (Recomendado): sistema de código/voucher
    resgatável, modelo Disque-Denúncia/Crime Stoppers — recompensa paga
    sem jamais vincular a um documento de identidade ou conta bancária
    pessoal do helper. A confirmar.
43. **Mecanismo de sinalização comunitária ("possível armadilha") fica
    documentado como visão, fora do MVP** — mesma tratativa dada a outras
    funcionalidades futuras (decisões 11, 12).
44. **Criptografia em repouso pra dados identificáveis em situações de
    risco de morte** — `AccountabilityLogEntry` (decisão 23) e qualquer
    dado que possa correlacionar identidade em denúncias de altíssimo
    risco (decisão 40) devem ser criptografados de forma que um vazamento
    ou invasão do banco de dados, isoladamente, não exponha identidade em
    texto claro. Chave de decriptação gerenciada separadamente da
    aplicação principal.
45. **Nenhum administrador isolado pode decriptar esses dados
    unilateralmente** — acesso exige (a) base legal documentada (ordem
    judicial/solicitação formal de investigação policial) OU emergência
    formalmente justificada (risco iminente à vida), **e** (b)
    autorização de pelo menos 2 papéis administrativos distintos (regra
    de duplo controle), com toda tentativa de decriptação permanentemente
    registrada em log de auditoria. ⚠️ Pesquisa preliminar — confirmar com
    advogado o enquadramento legal exato pra investigação policial no
    Brasil antes do lançamento, mesmo padrão das decisões 25/30/41.
46. **Nível de risco por categoria (RiskTier) não é hard-coded** — é um
    cadastro gerenciável por administrador em runtime (mesmo padrão do
    `tb_feature_flag` do setes-api: cache com TTL, fonte de verdade no
    banco, editável sem deploy de código). Um admin pode criar/atualizar/
    desativar regras de risco pra qualquer combinação de Categoria/
    Objeto-Sujeito sem alterar código.

## Fluxo end-to-end (denunciante e helper)

47. **Cada categoria tem formulário de detalhe próprio** (cachorro
    perdido, criança desaparecida, carro roubado, celular roubado,
    violência doméstica — cada um com campos específicos que ajudam o
    processo). Mesma filosofia não-hardcoded da decisão 46: o esquema de
    campos por categoria é configurável, não fixo no código, já que novas
    categorias podem surgir.
48. **Sistema de avaliação (rating) de helpers pelo denunciante ao
    finalizar a denúncia** — novo conceito, não coberto antes. Rating
    acumula na identidade INTERNA do helper (mesmo padrão da decisão 23 —
    log interno sem expor identidade), mesmo quando o helper é anônimo
    pro denunciante; isso constrói reputação ao longo do tempo sem quebrar
    anonimato, e pode alimentar o peso de confiança usado na decisão 27.
49. **Filtro de "gravidade" no lado do helper reutiliza o RiskTier**
    (decisão 46) — não é um conceito novo, a mesma configuração serve
    dois propósitos: regra de segurança (decisões 40, 41) e alerta de UX
    pro helper sobre o risco de se envolver.
50. **Após o encerramento de uma denúncia, usuários sem nenhuma interação
    registrada (nenhum Help Offer) veem só o status final** ("encerrada"),
    sem acesso a timeline, detalhes ou avaliações. Difere da decisão 18
    (helpers já vinculados continuam vendo tudo) — a restrição é
    especificamente para quem nunca interagiu.
51. **Botão de pânico notifica um grupo restrito de "respondedores
    autorizados"**, não o pool geral de helpers. Usuário solicita
    autorização pra virar respondedor; administrador aprova (mesmo padrão
    de cadastro administrável das decisões 46/49 — não hard-coded). Ao
    acionar o pânico, cada respondedor autorizado recebe a mensagem e a
    distância até a ocorrência.
52. ⚠️ **Pendência**: critérios de autorização pra virar "respondedor
    autorizado" ficam em aberto — decisão de uma rodada futura. Não
    bloqueia o desenho da estrutura (o mecanismo de autorização
    administrável já está decidido), só bloqueia o lançamento real do
    recurso até os critérios existirem.
53. **Integração real de despacho automático a autoridades (190/192/193
    ou central de monitoramento) fica documentada como intenção futura**,
    fora do MVP — mesmo tratamento das decisões 11 e 12. O MVP do pânico
    é a notificação aos respondedores autorizados (decisão 51), sem
    promessa de acionamento automático de autoridade.
54. **Chat denunciante-helper entra no MVP, mascarado** — texto simples,
    sem compartilhar contato direto (telefone, redes sociais), com as
    mesmas restrições de anonimato das categorias de risco (decisão 40).
    Novo Bounded Context, ainda não mapeado em `002-context-map.md`.
55. **Anonimato do helper (decisão 6) tem escopo total, não só em
    relação ao denunciante** — outros helpers na mesma denúncia também
    não veem a identidade de quem está anônimo. Refina a decisão 6.

## Painel administrativo

56. **Painel administrativo é um segundo app Flutter, web, no mesmo
    workspace** — `apps/admin`, ao lado de `apps/mobile`, reaproveitando
    `packages/core`, `packages/vgr_widgets`, `packages/vgr_validators`
    (mesmo padrão do `apps/web` do setes-app). Concentra toda
    funcionalidade administrativa já implícita nas decisões anteriores:
    gestão do RiskTier (46), formulários por categoria (47), autorização
    de respondedores do pânico (51-52), acesso de duplo controle aos
    dados criptografados (45), e configuração de monetização (39).

## Complemento ao fluxo

57. **Aviso legal de responsabilização é exibido antes de registrar
    qualquer denúncia** (não só no botão de pânico) — usuário confirma
    ciência de que falsa comunicação de crime é passível de
    responsabilização (referência: Código Penal, arts. 339 e 340). Texto
    exato e enquadramento fica com o mesmo tipo de pesquisa jurídica
    preliminar das decisões 25/30/39/45 — não bloqueia o MVP, mas precisa
    de advogado antes do lançamento.

## Intermediação de pagamento (painel administrativo)

58. **Pagamento ponta-a-ponta sem intermediação só é permitido fora das
    categorias de altíssimo risco (decisão 40)** — nessas categorias,
    intermediação é sempre obrigatória (preserva a garantia de anonimato).
    Nas demais categorias, admin/denunciante podem escolher intermediar
    ou deixar ponta-a-ponta, configurável por denúncia junto com a
    criticidade (mesmo cadastro administrável da decisão 46).
59. ⚠️ **Pendência de pesquisa comercial/técnica (não jurídica)**: qual
    Provedor de Serviços de Pagamento (PSP) licenciado usar pra
    intermediação com split de pagamento (ex: Mercado Pago, Pagar.me,
    Asaas, Iugu). Dono do produto quer pesquisar mais antes de decidir.
    Não bloqueia o desenho da arquitetura — ela já assume "PSP externo com
    API de split/marketplace" em vez do VGR virar instituição de pagamento
    (mitiga o risco regulatório da decisão 39); só o fornecedor específico
    fica em aberto.
60. **Esclarecimento da decisão 40: "identificação proibida" é em
    relação a OUTROS USUÁRIOS (denunciante, outros helpers), não em
    relação à própria plataforma.** Um helper registrado atuando em
    denúncia de altíssimo risco continua identificável internamente —
    dados protegidos pela criptografia + duplo controle das decisões
    44/45 — e isso é o que permite que o pagamento de recompensa seja
    processado normalmente pelo PSP. Só a exposição social dentro do app
    fica oculta (decisões 40, 55). O denunciante nunca sabe para quem
    está pagando; a plataforma sempre sabe.
61. **Decisão 42 (voucher/resgate anônimo) é rebaixada de requisito
    confirmado para opção documentada, não necessária no MVP** — a
    clarificação da decisão 60 resolve o caso geral (helper registrado,
    identidade oculta só dos outros usuários) sem precisar de trilha de
    pagamento alternativa. Voucher fica só como opção futura, caso surja
    um helper que recuse se registrar/fazer KYC mesmo assim — hoje a
    decisão 34 já barra recompensa nesse caso, categoria de risco ou não.

## Correção: botão de pânico é independente do fluxo de denúncia

62. **Correção de modelagem: o botão de pânico NÃO faz parte do fluxo de
    registro de denúncia.** É uma funcionalidade independente, acessível
    a qualquer momento por um menu — não uma pergunta binária na tela de
    categoria (como estava modelado antes). Revisa a decisão 51 e o
    fluxograma de validação.
63. **Botão de pânico tem dois níveis de acessibilidade, configuráveis
    pelo próprio usuário:**
    - **Padrão (todo usuário)**: acessível via menu a qualquer momento,
      sem configuração prévia — pensado pra quem testemunha algo
      acontecendo agora (assalto, violência) e quer alertar rápido, sem
      burocracia.
    - **Ativado/em destaque (opt-in, pra quem antecipa risco)**: usuário
      com risco iminente conhecido (ex: mulher com medida protetiva,
      idoso) pode ativar o botão pra ficar mais visível/acessível no app,
      e configurar antecipadamente quem recebe o alerta.
64. **Destinatário do alerta de pânico é configurável pelo usuário, com
    dois modos, não exclusivos entre si:**
    - **Plataforma** — pool de Respondedores Autorizados (decisão 51);
      desvio futuro pra polícia continua registrado como intenção
      (decisão 53, sem mudança).
    - **Contato pessoal de confiança** designado pelo próprio usuário
      (ex: familiar, amigo) — alternativa ou complemento ao pool geral,
      mais relevante pra quem já tem rede de apoio identificada (ex:
      idosos avisando familiares).
65. **Acionamento sem configuração prévia (uso "a frio", cenário de
    testemunha) vai direto pro pool de Respondedores Autorizados**
    (decisão 51), sem exigir mais informação do usuário no momento do
    clique — só ativa o alerta.

## Estratégia de execução do backlog

66. **Sempre que uma tarefa do app (mobile ou admin) depender de um
    endpoint da API que ainda não existe, pular para a API primeiro e
    implementá-lo antes de continuar** — sem perguntar a cada vez que
    isso acontecer. Mantém as duas frentes sincronizadas em vez de deixar
    o app bloqueado esperando.

## Autenticação do painel admin

67. **O painel admin (`apps/admin`) tem seu próprio login por
    e-mail/senha, independente dos provedores da decisão 31.** Decisão
    31 cobre login do denunciante/helper no app móvel (Google, Apple,
    Facebook, OTP por telefone) — não faz sentido para um painel
    administrativo interno. Cria-se `AdminAccount` (e-mail + senha com
    hash bcrypt) só para quem já é admin; não há autocadastro público,
    contas são semeadas/criadas manualmente (`scripts/seed-admin.ts` por
    enquanto). Endpoint `POST /auth/admin-login` retorna um JWT
    `{ userId, role: 'admin' }`, mesmo formato usado pelo resto da API.

## ⚠️ Pendências

Nenhuma. Rodada encerrada — Fase 0 fechada.

## Fora de escopo para esta fase

- Previsão de trajetória por modelo de velocidade + notificação push
  proativa (decisão 11) — visão documentada, implementar em fase futura.
- Categoria "policial validado" e seu fluxo de validação (decisão 12) —
  fase futura.
- Regras legais de recompensa/LGPD-equivalentes fora do Brasil (decisão 8)
  — modelo de dados preparado, regras não implementadas agora.

## Critérios de sucesso

1. Usuário consegue registrar uma denúncia escolhendo categoria + objeto/
   sujeito da taxonomia existente, ou criar uma tag livre quando nenhuma
   categoria existente se aplica (decisões 3, 9).
2. Usuário (mesmo anônimo) consegue visualizar denúncias próximas, ordenadas
   por mais recentes, dentro de um raio em km que varia por categoria da
   denúncia (decisões 2, 7).
3. Usuário consegue se candidatar como helper escolhendo um tipo de ajuda
   entre as opções pré-definidas (decisão 10).
4. Helper consegue escolher entre ajudar anonimamente, identificado sem
   recompensa, ou identificado com recompensa — sem que o sistema force
   identificação para quem não quer recompensa (decisões 4, 6).
5. Sistema exige cadastro completo apenas quando o helper opta por receber
   recompensa; helper anônimo ou sem recompensa não é bloqueado por
   cadastro (decisão 4).
6. Denunciante consegue oferecer recompensa opcional (monetária ou não) ao
   registrar/atualizar uma denúncia (decisão 1).
7. Em nenhuma tela, notificação ou log acessível ao usuário final a
   identidade de alguém que optou por anonimato é exposta (decisão 6).
8. O raio de busca nunca é um valor fixo global — é derivado da categoria da
   denúncia (decisão 7).
