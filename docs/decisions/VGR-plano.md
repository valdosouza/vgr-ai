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

    ⚠️ **Pendência FECHADA pela decisão 80**: mensagens de erro da API são
    somente em inglês — não há i18n de mensagem de erro no servidor, nem
    agora nem em fase futura.

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
    ⚠️ **REVISADA pela decisão 76** — passa a existir bloqueio de execução
    por jurisdição (Legal Gate). O que sobrevive desta decisão: o conjunto
    de regras *default* continua sendo o brasileiro; o que muda: deixa de
    ser o único e passa a ser enforçável/desligável por país.
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
    usuário. ⚠️ **Pendência FECHADA pela decisão 81**: a intermediação é
    executada por terceiro licenciado, não pelo VGR — o enquadramento na
    Lei 12.865/2013 deixa de recair sobre o projeto, **desde que** a
    restrição de custódia da decisão 81 seja respeitada.
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
    ⚠️ **FECHADA — e negada — pela decisão 82.** Já havia sido rebaixada
    pela decisão 61 (voucher como opção futura); a decisão 82 vai além e
    **proíbe** voucher e benefício não-monetário nas categorias críticas.
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
    ⚠️ **ENDURECIDA pela decisão 82**: nas categorias críticas o voucher
    deixa de ser "opção futura" e passa a ser proibido. Nas demais
    categorias esta decisão 61 continua valendo como está.

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

## Controles administrativos (módulos, menus, permissões, i18n)

Plano executivo desta frente: `AI\docs\plans\plano-controles-administrativos.md`
(mapa de reuso do setes-app/setes-api, fases 0–5). As decisões 68–71 registram
as diretrizes dadas pelo dono do produto; as escolhas em aberto estão na
rodada 1 de pendências abaixo.

68. **Instalação por país, single-schema.** Cada país pode requisitar uma
    instalação própria por questão de segurança doméstica; portanto NÃO se
    copia o multi-tenant do setes — sem `tb_institution`, sem `schema_name`,
    sem interpolação de schema nas queries. O runner de migração atual do VGR
    já atende.
69. **Sem licenciamento de interfaces.** Não existe "país compra uma coisa e
    não compra outra" — tudo vai no pacote; o que cada usuário vê e faz é
    controlado exclusivamente por permissão de usuário. NÃO se copia
    `tb_institution_has_interface` (o contrato comercial do setes).
70. **Sem superusuário.** Diferente do Produto de Gestão ERP, não há papel
    "super": o Admin é um usuário com privilégio na interface de administração
    de usuários/permissões, capaz de determinar quem acessa o quê. Bootstrap
    por seed (as contas admin existentes recebem todos os privilégios).
    Nenhum guard por role mágico — privilégio decide tudo.
71. **O modelo de permissões herda o desenho do setes** (decisão 15 aplicada a
    esta frente), com as simplificações 68–70: `tb_user`, `tb_privilege`,
    `tb_interface` (+ `tb_interface_has_privilege`), `tb_module`
    (+ `tb_module_has_interface`), `tb_user_has_privilege` (PK
    user × interface × privilege); menu montado pelo backend em
    `GET /api/core/menus`, filtrado pelo privilégio VIEW. Telas
    administrativas: Privilégios, Interfaces, Módulos/Menu (CRUD novo — o
    setes nunca implementou o cadastro de `tb_module`) e Usuários com aba de
    privilégios. Escopo: a equipe administrativa (`apps/admin`); os papéis do
    app móvel (decisões 4, 31) ficam fora do sistema de privilégios.

72. **Enforcement de privilégio no BACKEND, por endpoint** — divergência
    consciente do setes (onde `tb_user_has_privilege` só filtra o menu e a
    API confia no cliente). Middleware `requirePrivilege(interface,
    privilégio)` aplicado rota a rota (GET→VIEW, POST→INSERT, PUT→UPDATE,
    DELETE→DELETE), substituindo o `require-admin.middleware.ts` binário.
    JWT continua com payload mínimo (`userId`); os privilégios são
    consultados no banco com cache TTL (mesmo padrão do
    `feature-flag.middleware.ts` do setes). A API é a autoridade; menu e
    botões do app apenas refletem.
73. **Sessão do painel admin: JWT TTL 24h + "Manter conectado"** (padrão
    setes, sem refresh token no MVP). Com o checkbox marcado, o token
    persiste no navegador (`shared_preferences`/localStorage) e a sessão
    sobrevive ao refresh; desmarcado, fica só em memória. "Lembrar
    credenciais" grava apenas o e-mail, nunca a senha. Refresh token fica
    como evolução futura, se a operação exigir.
74. **`tb_admin_account` evolui para `tb_user`** (renomeada por migração,
    preservando as contas existentes) com as colunas novas: `name`,
    `active`, `locale`, `last_login_at`, `activation_key` (recuperação de
    senha), `deleted`. Evolui a decisão 67: o conceito `AdminAccount` dá
    lugar ao usuário de equipe governado por privilégios (decisão 70).
75. **Contas da equipe são criadas diretamente pelo Admin** na tela de
    Usuários (com senha inicial), sem fluxo de convite por e-mail no MVP —
    aposenta o `seed-admin.ts` como via ordinária (permanece só como
    bootstrap da primeira conta). Convite por e-mail com ativação fica
    documentado como opção futura.

## Legal Gate (bloqueio de execução por jurisdição)

Plano executivo desta frente: `AI\docs\plans\plano-legal-gate.md` (princípios,
modelo de dados, fases L0–L4). As decisões 76–79 registram as diretrizes dadas
pelo dono do produto; as escolhas em aberto estão na rodada 2 de pendências
abaixo. **Esta frente revisa a decisão 24.**

76. **A execução é bloqueável por jurisdição.** Existe um Legal Gate: cada
    *capacidade* do produto (anonimato, recompensa, intermediação de
    pagamento, retenção de dado de menor, rastreio de localização,
    transferência internacional, etc.) tem um estado declarado por país, e
    esse estado é enforçado pela API — não é documentação, é bloqueio.
    Revisa a decisão 24 (que previa lei brasileira sempre, sem geo-bloqueio)
    e realiza o que a decisão 8 já havia preparado no modelo de dados.
77. **A análise que alimenta o gate é produzida por IA, não por advogado.**
    O parecer jurídico deixa de ser pré-requisito do desenvolvimento e passa
    a ser um *upgrade posterior do mesmo registro*: a linha da regra tem um
    campo `review_state` que evolui de `ai_assessed` para
    `counsel_confirmed` sem tocar em código. Isso substitui o padrão atual
    das decisões 25, 30 e 39 ("confirmar com advogado antes do lançamento"),
    que hoje só tem os estados *esperar* ou *ignorar*.
    ⚠️ **Limite explícito do desenho**: a IA nunca escreve a regra ativa.
    Ela grava uma avaliação; uma pessoa com privilégio a promove a regra, e
    é o nome dessa pessoa que fica no registro. Análise de IA não é parecer
    jurídico e não transfere responsabilidade — o que protege a operação é
    ter havido controle explícito, base declarada, aprovação identificada e
    log imutável.
78. **Três motivos de bloqueio, tipificados e obrigatórios**: `no_control`
    (o produto ainda não tem o mecanismo que a lei exige), `legislation`
    (a lei local proíbe ou exige o que não temos) e `self_preservation`
    (o risco para a operação supera o benefício). Bloqueio sem motivo
    declarado não existe no modelo — a coluna é `NOT NULL`. O motivo
    `self_preservation` é de uso legítimo e registrado: é a via pela qual o
    produto se recusa a executar algo que o exponha, sem precisar fingir
    fundamento legal que não tem.
79. **Desenvolvimento e demonstração nunca são bloqueados.** Existe a
    jurisdição `SANDBOX`, na qual o default se inverte (capacidade sem
    regra é liberada) e toda resposta carrega marca de demonstração. Em
    qualquer jurisdição real o default é o oposto — capacidade sem regra
    ativa é bloqueada (fail-closed, mesmo princípio da decisão 72). A
    consequência prática é a pretendida: o produto pode ser mostrado ao
    mercado inteiro sem que isso afirme conformidade em lugar nenhum, e uma
    instalação real nasce desligada até alguém declarar por que pode ligar.

## Contrato de erro da API

80. **Mensagens de erro da API são somente em inglês** — não existe i18n de
    mensagem no servidor, nem no MVP nem em fase futura. Fecha a pendência
    aberta na decisão 17 e o item 1 da rodada 1. O que a API devolve é
    `{ error, code, fields? }` com `error` em inglês fixo; **o `code`
    (`shared/errors/error-codes.ts`) é o contrato de tradução** — quem
    traduz para o usuário final é o cliente (app móvel e `apps/admin`), pela
    chave do código, nunca pelo texto.

    Consequência que isto cria (item de execução, não decisão): o `code`
    deixa de ser um detalhe de diagnóstico e vira a chave de i18n do
    cliente. Hoje ele não serve para isso — cinco erros 409 semanticamente
    distintos compartilham `DUPLICATE`, e um deles ("You cannot delete your
    own account") se traduziria no app como "já existe". O catálogo precisa
    ganhar códigos próprios (mínimo: `IN_USE`, `SELF_LOCKOUT`,
    `BUSINESS_RULE`) e o campo `code` de `HttpError` precisa deixar de ser
    opcional. Detalhado em `AI\docs\plans\plano-erro-i18n.md`.

## Trilho de pagamento da recompensa

81. **A intermediação de pagamento é executada por terceiro licenciado
    (PSP/gateway), não pelo VGR — com integração própria preservada como
    possibilidade futura.** Fecha a pendência da decisão 39 (Lei
    12.865/2013): quem tem autorização do Banco Central é o terceiro; o VGR
    é provedor de tecnologia que orquestra o fluxo, não instituição de
    pagamento. Eleva a decisão: a **decisão 59** já operava com "PSP externo
    com split" como premissa de arquitetura, mas como premissa — agora é
    escolha registrada, com a restrição de custódia abaixo e o caminho da
    integração futura explicitado. A pendência de *qual* PSP (decisão 59)
    continua aberta e é independente desta.

    ⚠️ **A isenção é condicional, e a condição é de arquitetura**:
    delegar ao PSP só afasta o enquadramento se o VGR **não tiver custódia**
    — sem carteira, sem saldo, sem float, sem escrow em nome do projeto. Se
    o dinheiro parar em conta controlada pelo VGR, ainda que por instantes
    e ainda que o PSP esteja no fluxo, o enquadramento como arranjo de
    pagamento volta a ser discutível. Portanto: **split payment executado
    pelo PSP**, e a taxa da decisão 39 chega como perna do split — nunca
    como retenção de dinheiro que o VGR tenha segurado. A forma exata da
    custódia é o item 1 da rodada 3, e é a decisão que determina se o BACEN
    volta ou não ao problema.

    **A possibilidade futura não é um "depois a gente vê"** — ela já tem
    forma no desenho: o trilho vive atrás da Anti-Corruption Layer que o
    `README.md` previu para o subdomínio Reward, como uma porta
    `PaymentRail` com um adapter por provedor. Integrar o trilho próprio no
    futuro é acrescentar um adapter e virar uma regra no Legal Gate
    (`reward.intermediation.own`, hoje `blocked` por `no_control` até
    existir autorização), não reescrever o domínio.

    O enum `payment_mode_allowed` de `tb_fee_rule` **não muda**:
    `intermediated` passa a significar "intermediado por terceiro
    licenciado", e *quem executa* é assunto do adapter, não do modelo de
    domínio. Isso é deliberado — evita migração agora e evita outra quando
    o trilho próprio chegar.

82. **Nas categorias críticas (decisão 40), a recompensa — quando existe —
    é obrigatoriamente em dinheiro, via transferência/Pix pelo trilho
    intermediado. Voucher e benefício não-monetário são proibidos.**
    Fecha a pendência 42 negando-a e endurece a decisão 61 (que deixava o
    voucher como opção futura).

    Confirma e reforça o desenho de dois planos já estabelecido nas
    decisões 60 e 55: **a identificação vive na plataforma administrativa
    (`apps/admin`), e só nela; na plataforma operacional (`apps/mobile`) o
    anonimato é total.** O denunciante nunca sabe para quem paga; a
    plataforma sempre sabe. É a mesma natureza da decisão 23 (anonimato é
    social, não forense), aplicada ao dinheiro.

    **Por que benefício não-monetário é pior que dinheiro aqui** — é
    contraintuitivo, então fica registrado: todo benefício físico precisa
    ser *entregue*, e entrega exige endereço, ponto de retirada, encontro
    ou resgate presencial. Cada uma dessas coisas reidentifica o helper ou
    cria um canal de contato fora da plataforma, que é exatamente o que as
    decisões 40/41/55 existem para impedir. Pagamento em conta pelo PSP é
    o único trilho que se completa sem ponto de contato físico.

    Consequência sobre a decisão 1 (recompensa flexível, não
    necessariamente financeira): **ela não se aplica às categorias
    críticas** — ali a recompensa é dinheiro ou não existe.

    ⚠️ **Requisito que isto impõe à escolha do PSP (decisão 59)**: o
    registro do lado do pagador não pode nomear o recebedor. Em split de
    marketplace o extrato do denunciante mostra a plataforma, não o
    helper — mas isso **varia por PSP e por meio de pagamento** e deixa de
    ser detalhe comercial para virar critério de aceitação: um PSP cujo
    comprovante ao pagador exiba o nome do recebedor é inutilizável nas
    categorias da decisão 40.

## Contrato de erro da API (execução da decisão 80)

83. **Erro por campo também traduz por código: `fields[].code` +
    parâmetros estruturados.** `zodToFields` passa a emitir, para cada
    campo, um `code` estável derivado do `issue.code` do Zod (`REQUIRED`,
    `TOO_SHORT`, `TOO_LONG`, `INVALID_EMAIL`, `INVALID_FORMAT`,
    `INVALID_OPTION`…) e `params` estruturados quando houver valor (ex.:
    mínimo de caracteres) — o cliente traduz pelo código com a mensagem
    inglesa do Zod como fallback. Fecha a pendência 3 da rodada 1,
    viabilizando a promessa de UI traduzida da decisão 80 no erro que o
    usuário mais vê. Junto, executa-se o plano
    `AI\docs\plans\plano-erro-i18n.md`: códigos novos `IN_USE`,
    `SELF_LOCKOUT`, `BUSINESS_RULE`, `NOT_AVAILABLE`; `HttpError.code`
    obrigatório; reclassificação dos call sites colididos em `DUPLICATE`.

## Custódia do dinheiro da recompensa

84. **Custódia zero: o dinheiro nunca toca conta do VGR.** O PSP debita o
    denunciante e credita helper e VGR em pernas separadas da mesma
    transação (split); a taxa da decisão 39 chega como perna do split,
    nunca como retenção. Fecha o item 1 da rodada 3 e **torna incondicional
    a isenção da decisão 81** — sem titularidade de saldo de terceiros, não
    há o que enquadrar na Lei 12.865/2013. Escrow em nome do VGR e
    carteira/saldo interno ficam descartados; carteira permanece registrada
    como o conteúdo da capacidade `reward.intermediation.own`, bloqueada no
    Legal Gate até existir autorização (decisão 81).

    **Proibições de arquitetura que isto cria** — valem para todo código
    futuro do subdomínio Reward: nenhuma tabela de saldo/carteira/ledger de
    fundos de usuário, nenhuma etapa em que o valor fique "parado" sob
    controle do VGR, e `PaymentIntent` (task 30) não pode introduzir passo
    de retenção. O VGR registra *intenção* e *resultado* de pagamento;
    dinheiro é estado do PSP, nunca do nosso banco.

    **Critérios de aceitação que isto acrescenta à escolha do PSP
    (decisão 59)** — somados ao da decisão 82 (comprovante do pagador não
    nomeia o recebedor):
    1. API de split real, com **N recebedores** na mesma transação — a
       decisão 30(c) divide a recompensa entre helpers que cumprem a
       condição simultaneamente; split de 1 recebedor não atende.
    2. Pagamento ao helper sem exigir que o denunciante conheça qualquer
       dado do helper (decisões 40, 82).
    3. Pré-autorização com captura posterior, e uma forma de **consultar o
       estado vivo da reserva** — a decisão 85 tornou isso a fonte da
       verdade do selo exibido na denúncia, não um detalhe de cobrança. PSP
       que autorize mas não permita consultar/renovar a reserva não atende.

85. **A garantia é escolha do denunciante, e vira informação visível na
    denúncia.** Ao oferecer recompensa, o denunciante decide se pré-autoriza
    o valor (PSP bloqueia no meio de pagamento dele, captura na resolução —
    custódia zero preservada, decisão 84) ou não. A denúncia exibe esse
    estado, e cada lado assume conscientemente o seu risco: o helper que
    ajuda numa denúncia sem garantia assume o risco do calote; o denunciante
    que não garante assume o risco de não ser ajudado. Fecha o item 6 da
    rodada 3 — as três opções que estavam na mesa (garantir sempre, nunca
    garantir, ou pagar adiantado) viravam política única da plataforma;
    esta transforma o trade-off em informação de mercado e deixa os dois
    lados decidirem.

    **A consequência de engenharia é dura e não negociável: o selo tem de
    ser verdade a todo instante.** Uma pré-autorização de cartão expira
    (janela típica de 5 a 30 dias) e denúncia pode demorar mais que isso.
    Portanto o estado exibido **deriva da reserva viva no PSP, nunca de um
    booleano gravado no momento da oferta**. Se a reserva cai, a denúncia
    deixa de exibir a garantia — no mesmo instante. Uma denúncia que anuncia
    garantia sem lastro é pior que uma denúncia sem garantia nenhuma: é a
    plataforma mentindo para quem vai correr risco físico.

    **A obrigação existe nos dois casos** — isto precisa estar claro no
    texto do app. A promessa de recompensa da decisão 30 obriga o
    denunciante mesmo sem pré-autorização; o que muda entre garantida e não
    garantida é a *exequibilidade prática*, não a existência do dever. O
    app não pode dar a entender que a recompensa não garantida é opcional,
    sob pena de contradizer a decisão 30 e de informar mal o usuário sobre
    uma obrigação que ele de fato tem.

    ⚠️ **Cuidado com a palavra "garantida"**: nem a captura de uma
    pré-autorização é imune a estorno/chargeback. Chamar de "garantida" o
    que é "valor reservado" cria expectativa que a plataforma não controla
    inteiramente — risco de reclamação de consumidor mais tarde. O texto
    exato virou pendência (item 8 da rodada 3).

86. **Recompensa sem reserva é permitida nas categorias críticas, mas exige
    ciência explícita do helper antes de ele se oferecer.** Fecha o item 8
    da rodada 3. Segue o precedente que a decisão 34 já criou (helper
    anônimo é informado, antes de ajudar, que não poderá reivindicar a
    recompensa) — o produto informa e deixa decidir, em vez de proibir.

    **A ciência só é um controle se ficar registrada.** Fica gravada no
    próprio Help Offer — é o ato de se oferecer que a carrega — com
    timestamp e **a versão do texto que o helper efetivamente viu**. Se a
    redação mudar depois (item 7 da rodada 3 ainda vai defini-la), o
    registro precisa dizer o que estava escrito na hora, não o que está
    escrito hoje.

    **O passo é condicional, não universal**: só aparece quando a categoria
    é crítica **e** há recompensa **e** não há reserva. Ciência que aparece
    sempre vira clique automático e deixa de informar. E precisa ser um
    toque, não um formulário — categoria crítica é justamente onde a
    velocidade de resposta importa (decisões 7, 22).

    **O que se informa não é "você não vai receber"** — é que a plataforma
    não está segurando o dinheiro. A obrigação do denunciante existe do
    mesmo jeito (decisões 30, 85). Dizer o contrário seria informar mal o
    helper sobre um direito que ele tem.

    ⚠️ **Isto eleva o item 9 da rodada 3 de detalhe a requisito**: quem se
    ofereceu enquanto havia reserva nunca deu ciência nenhuma. Se a reserva
    expira depois, esses helpers passam a estar na situação que a decisão 86
    manda informar — sem terem sido informados. O tratamento de expiração
    tem de resolver isso, não só notificar.

87. ⚠️ **REVISADA pela decisão 95** — o mecanismo (A) pré-autorização morre
    junto com o cartão; resta só o (B), retenção no PSP via Pix, e a
    verificação de titularidade deixa de ser contingência para virar
    dependência bloqueante. O texto original fica como registro:

    **Dois mecanismos de reserva, aplicados por faixa de valor ou
    categoria** (análise em `AI\docs\plans\plano-garantia-recompensa.md`):
    **(A) pré-autorização** como padrão — o emissor bloqueia o limite, o
    dinheiro não sai da conta do denunciante, cancelar devolve sem estorno,
    e a janela real (5 a 30 dias) vira o selo *"reservado até DD/MM"*; e
    **(B) retenção no PSP** para os casos que justificam prazo longo, com o
    selo *"reservado até a resolução"*. Fecha a pergunta do item 9 sobre
    como reter sem custodiar: em ambos, o titular do dinheiro é o emissor ou
    o PSP — **nunca o VGR** —, e o VGR apenas instrui liberação ou
    devolução. Decisão 84 preservada; mediação é papel de quem instrui, não
    de quem guarda.

    ⚠️ **(A) é incondicional; (B) é contingente.** A retenção no PSP só
    existe se a titularidade do valor retido for do próprio PSP ou do
    recebedor. Vários PSPs implementam retenção em conta titularizada pelo
    marketplace — se for esse o caso do fornecedor escolhido, o VGR viraria
    titular de dinheiro de terceiro, a decisão 84 cairia e o BACEN voltaria
    junto. Isso vira **pergunta contratual explícita** na pesquisa da
    decisão 59, não presunção: *em nome de quem fica o dinheiro retido?*
    Se nenhum PSP responder de forma aceitável, o produto opera só com (A)
    e o selo sem prazo deixa de existir.

    **Consequência de arquitetura**: a porta `PaymentRail` da decisão 81
    passa a expor reserva como conceito — `reserve` / `capture` / `cancel`
    — com duas implementações; qual delas se aplica é **política**,
    resolvida fora do adapter. Nenhuma das duas introduz passo de retenção
    sob controle do VGR (proibição da decisão 84).

    ⚠️ **Nova pendência: quem define a faixa** (item 11 da rodada 3).

    ⚠️ **Tensão registrada**: (B) exige que o denunciante pague de fato na
    oferta. As categorias críticas (decisão 40) são as que mais justificam
    prazo longo e, ao mesmo tempo, as que menos toleram fricção na oferta —
    velocidade de resposta ali é requisito (decisões 7, 22). Não se resolve
    escolhendo o mecanismo; entra na decisão da faixa.

88. **O denunciante escolhe o mecanismo de reserva explicitamente.** Fecha o
    item 11 da rodada 3. ⚠️ **AJUSTADA pela decisão 95**: a escolha continua
    sendo dele, mas passa de três opções para duas — reservar via Pix ou
    ofertar sem reserva. Não há cadastro administrativo de faixa — a decisão
    87 falava em "faixa de valor ou categoria", e a resposta é que quem
    define a faixa é o dono do dinheiro, caso a caso. Uma tela
    administrativa a menos.

    **Isso colapsa a escolha da decisão 85 e esta numa pergunta só**, com
    três respostas, em vez de duas perguntas em sequência:
    *sem reserva* · *reservar até DD/MM* (pré-autorização) · *pagar agora e
    reservar até a resolução* (retenção no PSP). Apresentar como duas
    perguntas encadeadas seria fricção gratuita num fluxo que precisa ser
    rápido.

    **O conjunto de opções é dinâmico, não fixo.** Some some conforme o
    mecanismo B não exista (decisão 87 — verificação de titularidade) ou o
    Legal Gate bloqueie a capacidade na jurisdição (decisão 76). A tela
    monta a partir do que o trilho daquela instalação de fato oferece; nunca
    exibe opção que não vai funcionar.

    **Requisito de linguagem, não de layout**: as três opções precisam ser
    ditas no vocabulário de quem está registrando uma denúncia, não no de
    quem entende de meios de pagamento. "Pré-autorização" e "retenção" são
    palavras nossas, não do usuário. Texto entra no item 7 da rodada 3, que
    agora cobre o selo **e** as opções da oferta.

    ⚠️ **A confirmar na tela** (não muda a decisão, só qual opção nasce
    pré-selecionada): sugestão de default por categoria — crítica tende a
    demorar mais, o que favorece a reserva sem prazo —, sempre com o
    denunciante podendo trocar. Serve para reduzir o risco de escolha errada
    que motivou a alternativa descartada.

89. ⚠️ **PENDENTE DE REVISÃO pela decisão 95** — nasceu do vencimento da
    pré-autorização, que deixou de existir com a saída do cartão. Só
    permanece se a retenção de Pix no PSP tiver prazo máximo próprio
    (item 17 da rodada 3). Texto original:

    **Expiração da reserva avisa os dois lados, em momentos diferentes.**
    Fecha o item 9 da rodada 3. O denunciante é avisado **antes** do
    vencimento, com renovação em um toque. Se expirar, a denúncia perde o
    selo (obrigação da decisão 85 — o selo deriva da reserva viva) e os
    helpers **já vinculados** recebem, como evento na timeline da
    decisão 19, a mesma informação que a decisão 86 exige de quem entra sem
    reserva. **Informa, não desvincula, não bloqueia** — quem quiser
    continuar ajudando continua.

    Fecha o buraco aberto pela decisão 86: quem se ofereceu enquanto havia
    reserva nunca deu ciência nenhuma e, sem este aviso, passaria a estar
    exatamente na situação que a 86 manda informar sem nunca ter sido
    informado. Quem chegar depois da expiração passa pelo fluxo normal de
    ciência pré-oferta.

    O evento registra **a versão do texto exibido**, pelo mesmo motivo da
    decisão 86 — o que vale é o que a pessoa leu na hora. E a notificação
    não pode revelar nada sobre os outros helpers, para não furar a
    decisão 41 (sinais de engajamento ocultos nas categorias críticas).

    ⚠️ **Isto cria o primeiro job agendado da API** — hoje não existe
    nenhum (`api/scripts` só tem migração e seed). Vira o item 13 da
    rodada 3. A antecedência do aviso é parâmetro de configuração, não
    constante em código (mesmo princípio da decisão 46).

90. **Trabalho agendado roda in-process, com `node-cron`, registrado na
    subida do servidor.** Fecha o item 13 da rodada 3. ⚠️ **A decisão 95
    removeu o gatilho que a motivou** (varredura de pré-autorização perto do
    vencimento). A escolha técnica continua válida e provavelmente será
    necessária de qualquer forma — retenção com prazo (item 17), lembretes,
    limpeza de dados da decisão 25 —, mas **não há mais urgência**: não
    construir antes de existir um job real para rodar. Escolhido pelo mesmo
    critério da decisão 68: o VGR é uma instalação por país, não uma frota —
    o cenário em que job in-process é adequado. Fila dedicada (Redis) e
    agendador externo ficam documentados como evolução, a primeira se a
    lista de trabalho assíncrono crescer (decisões 26, 28, push), o segundo
    se a operação passar a exigir execução independente do serviço web.

    **Onde mora**: `src/gateway/scheduler.ts`, simétrico ao
    `src/gateway/router.ts` — o gateway já é o ponto de composição que
    conhece todos os módulos, e assim nenhum módulo precisa importar outro
    (regra do `ARCHITECTURE.md`). Cada job é uma função do módulo dono,
    registrada ali.

    **Guardas obrigatórias**, porque job in-process erra de formas
    silenciosas: não subir sob `NODE_ENV=test` (senão os 112 testes passam a
    disparar varredura), não subir durante migração, e uma trava de
    instância única — sugestão a confirmar na implementação: linha de lease
    com timestamp no banco, de modo que uma segunda instância simplesmente
    pule a execução em vez de duplicar notificação. A antecedência do aviso
    da decisão 89 é configuração, não constante.

91. **O VGR contrata o PSP e figura como facilitador de marketplace.**
    Fecha o item 2 da rodada 3. É o arranjo que o split da decisão 84
    pressupõe, é o que permite cobrar a taxa da decisão 39 automaticamente
    como perna do split, e é o que faz o extrato do pagador mostrar a
    plataforma em vez do helper — requisito de anonimato das decisões 58 e
    82, não conveniência. A alternativa (cada denunciante virando cliente do
    PSP) foi descartada: sem o VGR na transação não há taxa automática, o
    recebedor volta a poder aparecer no extrato do pagador, e cada
    denunciante teria de fazer onboarding no PSP antes de ofertar.

    **O que o VGR assume junto**: obrigações contratuais de facilitador
    perante o PSP — conhecer os usuários, responder pelos fluxos que
    intermedia e, principalmente, figurar como parte em contestação de
    cobrança. Isso não conflita com a decisão 84: ser *parte* da transação é
    diferente de ser *titular* do dinheiro.

    ⚠️ **Nova pendência: quem absorve o chargeback** (item 14). É o custo
    escondido deste arranjo, e ele tem uma torção específica do VGR — se o
    denunciante contestar depois do helper já ter sido pago, o caminho
    normal de um marketplace seria cobrar do recebedor, mas nas categorias
    críticas o recebedor é justamente quem a plataforma não pode expor nem
    perseguir (decisões 40, 82). A garantia de anonimato tem um preço
    financeiro, e ele precisa ter dono declarado.

92. **Recompensa liberada não tem retorno, e isso é dito explicitamente ao
    denunciante antes de ele ofertar.** O aviso é aceito e registrado no ato
    da oferta, com a versão do texto exibido (mesmo padrão das decisões 86 e
    89). Não é política inventada pela plataforma: é a natureza da promessa
    de recompensa da decisão 30 — cumprida a condição, a obrigação está
    formada e não cabe revogação.

    **Escopo exato, porque a frase solta se contradiz com a mediação**: o
    que não tem retorno é a recompensa **liberada após a condição
    cumprida**. Antes disso o dinheiro volta normalmente — na
    pré-autorização, cancelando a reserva não há nem cobrança; na retenção
    no PSP, denúncia não resolvida devolve ao denunciante. É exatamente o
    "em alguns casos o valor é devolvido" que motivou a decisão 87. Sem esse
    recorte, o aviso proibiria a devolução que o próprio desenho promete.

    ⚠️ **O que o aviso resolve e o que não resolve** — precisa estar claro
    para não criar falsa segurança: contestação de cobrança é acionada no
    emissor do cartão, não na plataforma, e termo de uso não vincula o
    emissor. O que o aviso explícito e registrado faz é servir de **prova na
    contestação** (divulgação clara + condição cumprida + aceite registrado)
    e reduzir contestação de má-fé por ambiguidade. Não impede o débito.

    ⚠️ Enquadramento do aviso perante o CDC (inclusive o direito de
    arrependimento do art. 49, cuja aplicabilidade a uma promessa de
    recompensa a terceiro é discutível) segue o padrão da decisão 77: vira
    item declarado no Legal Gate, não bloqueio de lançamento.

## Interfaces kind 'R' (fecha a rodada 1)

93. ℹ️ *Este número foi disputado: outra frente numerou uma decisão de
    chargeback como 93 no mesmo dia. Resolvido em favor desta, que já estava
    citada em código; a outra virou a **decisão 102**.*

    **`kind` 'R' é ativado já — recurso permissionável que nunca vai ao
    menu.** Contraria a assunção provisória da rodada 1 ("só 'T' no MVP"),
    por escolha explícita do dono do produto. No VGR (sem licenciamento —
    decisão 69), um 'R' cataloga um SUB-RECURSO de tela (aba, ação
    especial) com privilégios próprios, concedíveis por usuário na mesma
    matriz da tela de Usuários; `GET /api/core/menus` continua filtrando
    `kind = 'T'`. Primeiro 'R' real, nascendo junto (migração 020):
    **`user_privileges`** — a aba "Privilégios de Acesso" da tela de
    Usuários vira recurso próprio, separando *editar dados de usuário*
    (interface `users`) de *conceder acesso* (`user_privileges`); conceder
    passa a exigir os dois privilégios (semântica E, guard em camadas).
    Consequência estrutural: o `SessionAccess` do app deixa de ser
    alimentado pela árvore do menu (que só tem 'T') e passa a consumir o
    novo `GET /api/core/permissions` (T + R), com o menu como fallback.

102. **Chargeback que prospera é repassado ao helper fora das categorias
    críticas; nas críticas o VGR absorve.** Fecha o item 14 da rodada 3.

    ⚠️ **Número fora de ordem, e o motivo fica registrado**: esta decisão
    nasceu numerada 93, colidindo com a decisão 93 (`kind` 'R'), que foi
    tomada em paralelo no mesmo dia. Duas frentes numeraram ao mesmo tempo a
    partir do mesmo último número conhecido. A colisão foi resolvida em
    favor do `kind` 'R', que já estava **citado em 11 arquivos de código e
    numa migração** — mover aquele número exigiria editar código já testado
    e quebraria a rastreabilidade que a numeração existe para dar. Esta aqui
    só era citada em documentos. Fica no lugar temático (entre 92 e 94, onde
    a narrativa do chargeback está), com o número certo. Nas
    categorias comuns o helper é identificado e responde pela devolução como
    em qualquer marketplace; nas críticas não há a quem cobrar sem violar as
    decisões 40 e 82, então a perda é da plataforma — é o preço da garantia
    de anonimato, e ele fica onde a garantia foi dada.

    **A regra ramifica por RiskTier**, o que faz do módulo de pagamento mais
    um consumidor do `shared/risk/risk-tier.service.ts` que ainda não foi
    extraído (mesma extração pendente que a `monetization-config` espera).

    **O helper precisa ser avisado disso antes de aceitar a recompensa** —
    mesmo padrão das decisões 86, 89 e 92: divulgação clara, aceite
    registrado, versão do texto guardada. Sem isso o repasse é surpresa, e
    surpresa financeira em cima de quem ajudou é pior para o produto do que
    a perda evitada.

    ⚠️ **Limite prático, registrado para não virar ilusão**: o helper já
    recebeu por Pix/transferência e não há débito automático sobre ele. Na
    prática o repasse depende de cobrança ou de compensação em recompensa
    futura, e boa parte será irrecuperável. O efeito real da decisão é criar
    **direito de regresso** e desestimular conluio — não garantir
    recuperação. Financeiramente, o VGR ainda deve provisionar como se
    absorvesse.

    ⚠️ **Nova pendência: prazo entre resolução e repasse ao helper**
    (item 15). É o controle que realmente limita a exposição — contestação
    que chega antes do pagamento apenas cancela o pagamento, sem nada a
    recuperar de ninguém.

94. ⚠️ **ESVAZIADA pela decisão 95** — Pix é irrevogável, não há janela de
    contestação a aguardar, então o repasse ao helper pode ser rápido e o
    custo registrado abaixo (helper de categoria crítica esperando semanas)
    deixa de existir. A regra sobrevive apenas se e enquanto houver
    instrumento com janela de contestação, o que hoje não é o caso. Texto
    original:

    **O repasse ao helper só ocorre depois da janela de contestação do meio
    de pagamento.** Fecha o item 15 da rodada 3. Exposição a chargeback
    praticamente nula e provisionamento previsível: contestação que chega
    antes do repasse apenas cancela o repasse, e o direito de regresso da
    decisão 102 quase nunca precisa ser exercido.

    **Duas condições sem as quais esta decisão fere o produto:**

    1. **O prazo é dito ao helper antes de ele se oferecer** — mesmo padrão
       de divulgação das decisões 86, 92 e 102. Prazo que aparece só na hora
       de receber é armadilha; prazo conhecido desde o início é regra do
       jogo.
    2. **O prazo é do instrumento, não do produto.** Janela de contestação
       existe em cartão; **Pix é irrevogável** — a devolução por Pix (MED)
       cobre fraude, não arrependimento, e tem janela própria muito menor.
       Ou seja: recompensa paga via Pix pelo denunciante praticamente não
       tem exposição, e segurar o helper por semanas nesse caso seria
       penalizá-lo por um risco que não existe. Confirmar o
       comportamento atual disso na pesquisa da decisão 59 — é área que
       muda rápido — e derivar o prazo do instrumento efetivamente usado.

    ⚠️ **Custo que fica registrado**: nas categorias críticas o helper
    arrisca integridade física e passa a esperar semanas para receber. É a
    combinação mais dura do desenho e é onde o mecanismo de recompensa mais
    corre risco de simplesmente não atrair ninguém. A saída provável está na
    condição 2 (Pix rápido) e em liberação parcial antecipada, que fica
    documentada como evolução, não MVP.

    ⚠️ **Nova pendência: prazo diferente por instrumento?** (item 16) — a
    condição 2 acima é requisito técnico ou vira regra de produto explícita.

95. **Só Pix. Cartão de crédito sai do escopo.** Princípio declarado pelo
    dono do produto: *a ideia é ajudar pessoas, não criar passivo para a
    empresa*. O denunciante que quiser o selo retém o valor via Pix; quem
    não retém, não tem selo. Fecha o item 16 da rodada 3 e **revisa boa
    parte do trilho** — para melhor, porque a maior parte da complexidade
    acumulada nas decisões 87–94 existia por causa do cartão:

    - **Decisão 87 — mecanismo A (pré-autorização) morre.** Pré-autorização
      é recurso de cartão. Resta só o mecanismo B, retenção no PSP, agora
      alimentada por Pix. Um mecanismo, não dois.
    - **Decisão 88 — a escolha do denunciante passa de três opções para
      duas**: reservar via Pix, ou ofertar sem reserva. A decisão em si
      (quem escolhe é o denunciante) continua valendo.
    - **Decisões 89 e 90 — perdem o gatilho.** Ambas nasceram do vencimento
      da pré-autorização (janela de 5 a 30 dias), que deixou de existir.
      Ficam pendentes de revisão, não canceladas — ver item 17.
    - **Decisão 94 — deixa de custar caro.** Pix é irrevogável, então não
      há janela de contestação a aguardar: o repasse ao helper pode ser
      rápido. Cai junto o custo que a 94 registrava como o ponto mais duro
      do desenho — helper de categoria crítica esperando semanas.
    - **Decisão 102 — vira caso de borda.** Sem chargeback, o repasse ao
      helper só entraria em cena numa devolução por MED, que cobre fraude e
      não arrependimento. A regra continua escrita; a frequência esperada
      cai a quase zero.
    - **Decisão 92 — fica mais forte.** "Recompensa liberada não retorna"
      deixa de ser só termo de uso e passa a ser propriedade do trilho.

    ⚠️ **O que isto torna crítico**: a verificação de titularidade que a
    decisão 87 tratava como contingência (*em nome de quem fica o dinheiro
    retido?*) vira **dependência bloqueante**. Antes havia o mecanismo A
    como alternativa se nenhum PSP respondesse de forma compatível com a
    decisão 84; agora não há. Se todo PSP disponível só retiver em conta
    titularizada pelo marketplace, o produto fica sem selo de reserva —
    ou quebra a custódia zero. Isso sobe ao topo da pesquisa da decisão 59.

    ⚠️ **Fricção que a escolha assume**: com Pix o dinheiro sai da conta do
    denunciante na hora da oferta — não é bloqueio de limite, é pagamento.
    Denúncia não resolvida exige devolução de verdade, não simples
    cancelamento. É o preço de eliminar o passivo, e está aceito.

    ⚠️ A palavra "garantida" continua sendo o ponto aberto do item 7 (a
    plataforma garante *reserva*, não *recebimento*) — sem relação com esta
    decisão, mas o selo agora é um só, o que simplifica o texto.

96. **Um adapter de pagamento por jurisdição, atrás da porta `PaymentRail`.**
    Fecha o item 3 da rodada 3. Coerente com a decisão 68 (instalação por
    país, soberania doméstica) e com o Legal Gate (decisão 76): o trilho é a
    peça mais local que existe, e a decisão 95 acabou de amarrar o produto
    ao Pix, que só existe no Brasil. PSP global único foi descartado —
    concentraria o fluxo financeiro de todos os países num mesmo terceiro,
    contradizendo o motivo da decisão 68, e criaria dependência sem plano B
    se esse fornecedor recusasse o arranjo de titularidade da decisão 84.

    **Guarda de arquitetura que isto exige**: nenhum conceito de Pix pode
    vazar para o domínio. Nada de `pixKey` em entidade, DTO ou tabela do
    subdomínio Reward — o domínio fala em referência de instrumento de
    recebimento, e só o adapter brasileiro sabe que aquilo é uma chave Pix.
    Sem essa disciplina a porta é decorativa e o segundo país vira reescrita,
    que é exatamente o que a Anti-Corruption Layer da decisão 81 existe para
    evitar.

    Consequência operacional aceita: cada país novo é um contrato, uma
    homologação e um conjunto de testes a mais.

97. **País sem PSP integrado bloqueia apenas a recompensa monetária.** Fecha
    o item 4 da rodada 3. A capacidade `reward.monetary` fica bloqueada por
    `no_control` naquela jurisdição (decisões 76, 78), enquanto denúncia,
    ajuda e recompensa não-monetária (decisão 1 — favor de vizinhança,
    reciprocidade, benefício de comerciante) seguem funcionando. O país
    entra no ar com o produto inteiro menos o dinheiro.

    **Precisão sobre "liga sozinho"**: são dois portões independentes, e
    ambos precisam estar abertos — a **regra legal**, que continua sendo
    promovida por uma pessoa (decisões 77, 82), e a **disponibilidade
    técnica**, que é existir adapter configurado (decisão 96). Ter adapter
    não libera nada por si; o que a decisão garante é que ligar não exige
    release de código, e não que ligue sem alguém decidir.

    **Consequência a aceitar**: nas categorias críticas a decisão 82 exige
    dinheiro ou nada. Logo, num país sem PSP, denúncia crítica simplesmente
    não tem recompensa — não há o fallback não-monetário ali, porque a 82 o
    proibiu de propósito.

98. **Mediação é capacidade própria do Legal Gate: `reward.mediation`.**
    Fecha o item 12 da rodada 3. Instruir a liberação de dinheiro retido de
    terceiro, cobrando taxa por isso (decisão 39), é o ponto do trilho que
    mais se aproxima de prestar serviço de pagamento — e a decisão 77 manda
    declarar esse tipo de coisa por país em vez de presumir. Como
    capacidade, nasce bloqueada onde ninguém analisou, tem base declarada
    onde é liberada, e pode ser desligada num país sem mexer no resto.

    **Disciplina que vem junto**, e sem a qual a capacidade é fachada:
    critérios de mediação **publicados antes do caso** (mediador que decide
    por critério não declarado é fonte de reclamação; declarado, é regra do
    jogo), decisão registrada em log imutável no padrão da decisão 76, e via
    de contestação. Tela administrativa com privilégio próprio no modelo das
    decisões 71/72; duplo controle da decisão 45 é o candidato natural acima
    de um valor.

    ⚠️ **Dependência entre capacidades, que o catálogo precisa suportar**:
    bloquear `reward.mediation` num país sem bloquear `reward.monetary`
    deixaria a plataforma aceitando reserva que não pode liberar — dinheiro
    de terceiro preso sem saída, que é o pior estado possível e justamente o
    que a decisão 84 quer evitar. Regra: **`reward.monetary` exige
    `reward.mediation` liberada na mesma jurisdição**. O Legal Gate passa a
    precisar do conceito de capacidade dependente, nem que seja como
    validação na promoção da regra.

99. **O gatilho da integração própria fica declarado desde já.**
    `reward.intermediation.own` (decisões 81, 76) só sai de `blocked`
    mediante **(a)** autorização do Banco Central — ou equivalente na
    jurisdição — e **(b)** promoção da regra no Legal Gate por duplo
    controle (decisão 45). Fecha o item 10 da rodada 3. O valor de decidir
    agora é decidir sem pressa: no dia em que a carteira própria virar
    prioridade comercial, a condição já estará acordada em vez de negociada
    com prazo em cima.

    ⚠️ **A autorização não relaxa a decisão 84 automaticamente.** As
    proibições de arquitetura da 84 — nada de tabela de saldo, carteira ou
    ledger de fundos de usuário — foram escritas em termos absolutos de
    propósito. Autorização obtida num país habilita a capacidade **naquele
    país**; mexer nas proibições exige decisão nova e explícita. Sem essa
    trava, basta uma licença em uma jurisdição para alguém introduzir
    carteira no código de todas.

100. **Contrato funcional da reserva, em uma frase**: o denunciante paga por
     Pix, **o PSP retém o valor**, e o VGR apenas **instrui o desfecho** —
     caso encerrado, o dinheiro vai para o(s) helper(s) ou volta para o
     denunciante. Consolida o mecanismo que sobrou da decisão 87 depois da
     95, com o papel de facilitador da 91 e a mediação da 98, e é a
     descrição que vai para a mesa do PSP.

     Três coisas que esta formulação fixa e que precisam sobreviver a
     qualquer fornecedor escolhido:

     1. **Quem retém é o PSP, não o VGR** (decisão 84). O VGR emite
        instrução; nunca recebe, nunca segura, nunca movimenta.
     2. **"Pagar os helpers", no plural.** A decisão 30(c) divide a
        recompensa entre helpers que cumprem a condição simultaneamente —
        a liberação precisa aceitar N recebedores numa mesma instrução, e a
        taxa da decisão 39 sai como mais uma perna do mesmo split.
     3. **Devolver é desfecho de primeira classe**, não exceção. Denúncia
        não resolvida devolve ao denunciante; isso é o que a decisão 92
        preserva ao recortar o "não tem retorno" para depois da condição
        cumprida.

     ⚠️ **A pergunta que continua bloqueante**: "o PSP retém" descreve o
     desenho, não a titularidade. Em nome de quem fica o valor retido decide
     se este contrato é compatível com a decisão 84 ou se a derruba —
     primeira pergunta do checklist em
     `AI\docs\plans\plano-psp-requisitos.md`.

101. **O selo é binário: ou a denúncia tem "recompensa garantida", ou não tem
     selo nenhum.** Fecha o item 7 da rodada 3 e, com ele, a rodada inteira.
     Cada lado assume o seu risco — o denunciante que não reserva assume o
     risco de não ser ajudado, o helper que ajuda sem selo assume o risco de
     não receber (decisão 85, reafirmada).

     **Não existe rótulo negativo.** O segundo estado é a *ausência* do selo,
     não um "sem garantia" escrito na tela. Isso resolve sozinho metade da
     objeção que estava registrada: "sem garantia" seria lido como "pode não
     pagar, e tudo bem", contradizendo a decisão 30 — ausência de selo não
     diz nada disso, só não afirma nada.

     **O que o selo garante, e precisa estar no texto explicativo por trás
     dele**: que o **valor está reservado** e será liberado a quem cumprir a
     condição. Não que um helper específico vá receber — quem decide se a
     condição foi cumprida é a mediação (decisão 98). A palavra "garantida"
     fica no rótulo; o escopo exato fica a um toque de distância. É o que
     mantém a promessa verdadeira sem transformar o selo num parágrafo.

     ⚠️ **Risco assumido conscientemente**: no Brasil a oferta vincula quem
     a faz (CDC, arts. 30 e 35), e "garantida" é palavra da plataforma, não
     do denunciante. Diferente do desenho anterior, aqui há lastro real — o
     dinheiro está retido no PSP (decisão 100) —, o que torna a afirmação
     defensável em vez de vazia. O enquadramento segue o padrão da
     decisão 77: entra como item declarado na avaliação do Legal Gate por
     jurisdição, não como bloqueio de lançamento.

     A ciência da decisão 86 continua sendo o mecanismo que informa o helper
     nas categorias críticas sem selo — o selo diz o que existe, a ciência
     diz o que falta.

## Legal Gate — rodada 2

103. **A unidade bloqueável é a capacidade — o verbo do domínio.** Fecha o
     item 1 da rodada 2. Nomes como `reward.monetary`, `reward.mediation`,
     `report.anonymous`, `minor.data_retention`, `data.cross_border`:
     estáveis diante de refactor, legíveis por quem promove a regra (que é
     gestor, não desenvolvedor) e independentes de transporte — valem para
     HTTP, para a fila offline (decisão 28) e para job agendado (decisão 90),
     que endpoint nenhum cobriria. Endpoint e categoria de denúncia foram
     descartados: o primeiro espalha um mesmo risco por várias rotas e ignora
     o que não passa por HTTP; a segunda erra o alvo, porque o risco legal
     está na ação e não no assunto — e o eixo categoria já tem dono, o
     RiskTier da decisão 46.

     Convenção de nome: `domínio.ação[.qualificador]`, minúsculo, separado
     por ponto. Catálogo inicial em `plano-legal-gate.md` §5, já alimentado
     pelas decisões 97, 98 e 99 — que citaram capacidade por nome antes
     mesmo desta pendência ser decidida.

     **Duas guardas sem as quais o gate é decorativo:**

     1. **Capacidade desconhecida bloqueia.** Consulta a uma chave que não
        existe no catálogo — erro de digitação, capacidade removida — é
        tratada como bloqueada, nunca como liberada. Um typo em
        `reward.moentary` não pode virar liberação silenciosa.
     2. **Capacidade catalogada sem chamador é dívida, não proteção.** Todo
        item do catálogo precisa ter ao menos um ponto de chamada real;
        verificação automatizada na fase L0, enquanto o catálogo ainda cabe
        num arquivo.

104. **Fail-closed: capacidade sem regra ativa está bloqueada.** Fecha o item
     2 da rodada 2. `unreviewed` se comporta como bloqueado em qualquer
     jurisdição real — só a `SANDBOX` inverte (decisão 79). Mesmo princípio
     do `requirePrivilege` (decisão 72) e é o que dá sentido ao motivo
     `no_control` da decisão 78: o produto se recusa a executar o que
     ninguém avaliou. Instalação nova nasce desligada e é destravada
     capacidade por capacidade, com base declarada.

     ⚠️ **"Sem regra" e "não consegui consultar" são coisas diferentes**, e
     tratar as duas igual tem consequência séria: a partir da fase L1 o
     catálogo mora no banco, e uma queda de banco desligaria de uma vez toda
     capacidade bloqueável — num produto de segurança pública isso é apagão,
     não prudência. Na L0 o problema não existe (catálogo em código,
     jurisdição por variável de ambiente, nenhuma dependência de banco);
     a partir da L1 vira escolha, registrada como item 9 da rodada 2.

105. **A jurisdição é a da instalação, e a divergência é eliminada por
     construção: cada instalação atende apenas quem está no seu país.**
     Fecha o item 3 da rodada 2. Em vez de detectar em tempo de execução que
     o titular pertence a outro regime e escalar para a regra mais
     restritiva, o produto impede que a situação exista. Consequência
     pretendida: **LGPD e GDPR ficam isolados**, cada instalação
     respondendo a um regime só.

     ⚠️ **Precisão que muda o mecanismo de controle**: GDPR (art. 3º) e LGPD
     (art. 3º) não se acionam por *nacionalidade*, e sim por o titular estar
     **no** território — o GDPR alcança quem está na União, não quem é
     cidadão europeu. Logo o controle correto não é "ser do país", é
     **estar no país**. Isso é uma boa notícia: o VGR já é um produto
     baseado em localização (decisão 7 — raio dinâmico a partir da posição
     atual), então o dado que a lei usa é o mesmo que o produto já precisa
     ter. E resolve o caso que "ser do país" não resolveria — o denunciante
     anônimo da decisão 32, de quem não se verifica nacionalidade nenhuma.

     **Denúncia de abrangência internacional** passa a exigir colaboração
     entre instalações — documentada como visão de futuro, mesmo tratamento
     das decisões 11 e 12, fora do escopo atual.

     **Efeito no plano do Legal Gate**: a fase L4 (sinal de jurisdição do
     titular e escalonamento para a regra mais restritiva) **deixa de
     existir**, e a correção técnica registrada no §4 do
     `plano-legal-gate.md` — de que a decisão 68 não produz isolamento legal
     — passa a valer apenas *se* este controle de localização não for
     implementado. Com ele, a decisão 68 de fato isola.

     ⚠️ **Nova pendência: como se controla "estar no país"** (item 10) — não
     bloqueia a L0.

106. **Escopo imediato do Legal Gate: L0 e L1 juntas.** Fecha o item 8 da
     rodada 2. Entrega de uma vez o gate enforçando (shared + middleware +
     catálogo) **e** administrável sem deploy (migração 022 — 020 e 021 já
     foram usadas pela decisão 93 —, tabelas de jurisdição/capacidade/regra/
     auditoria, módulo `legal-policy`, cache TTL com kill switch de TTL
     zero). Evita construir o catálogo hardcoded para reescrevê-lo semanas
     depois.

     **Consequência imediata**: as pendências 4 (quem ativa regra), 5
     (expiração) e 9 (falha de consulta) deixam de ser adiáveis — bloqueiam
     código agora. A 6 (dado congelado) e a 7 (registro da avaliação de IA)
     seguem sem bloquear: a 6 é comportamento de leitura que pode nascer
     depois, e a 7 pertence à fase L2.

107. **Promoção de regra legal exige privilégio dedicado e duplo controle.**
     Fecha o item 4 da rodada 2. Interface `legal-rules` no modelo das
     decisões 71/72; a promoção segue o fluxo do módulo dual-control com o
     papel de aprovador separado que a decisão 93 já criou (recurso
     `dual_control_approval`) — quem propõe não aprova. Coerente com a
     decisão 99, que já exigia duplo controle para a promoção mais sensível
     (`reward.intermediation.own`); um regime só para todo ato do mesmo
     tipo. Uma regra errada aqui liga capacidade proibida num país ou
     desliga o produto — é o caso de uso mais forte do duplo controle no
     produto inteiro.

     **Exceção deliberada, no outro sentido**: o kill switch de jurisdição
     (`operational_state` → `suspended`, decisão do plano §7) é acionável
     por **uma** pessoa com o privilégio — emergência não espera segundo
     aprovador. Religar (`suspended` → `live`), sim, exige o fluxo completo
     de duplo controle. Desligar rápido, religar devagar.

108. **Toda regra legal expira — prazo padrão de 180 dias, configurável por
     regra.** Fecha o item 5 da rodada 2. Vencida, a capacidade volta a
     `unreviewed` e portanto a bloqueada (decisão 104); renovar é reavaliar
     e promover de novo, com o duplo controle da decisão 107. Vale para
     qualquer `review_state` — análise confirmada por advogado também
     envelhece, porque a lei muda independente de quem analisou; o que o
     `counsel_confirmed` pode ter é prazo maior, nunca isenção de prazo.

     **Encaixes que esta decisão fecha:**
     - O campo `expires_at` de `tb_legal_rule` (plano §6) deixa de ser
       opcional — `NOT NULL`.
     - O aviso de vencimento próximo é um job do scheduler da decisão 90,
       que ganha aqui seu segundo caso de uso (o primeiro, da decisão 89,
       ficou condicionado ao prazo de retenção do PSP).
     - A expiração **não é** o kill switch: regra vencida bloqueia a
       capacidade específica com motivo `no_control` (voltou ao estado "não
       avaliado"), sem tocar no `operational_state` da jurisdição.
     - País esquecido desliga sozinho, capacidade por capacidade — é o
       fail-closed da decisão 104 operando no tempo, e é comportamento
       pretendido, não acidente.

109. **Falha na consulta ao gate: serve o último estado conhecido por uma
     janela limitada, depois bloqueia.** Fecha o item 9 da rodada 2 (o
     último bloqueante de código). O cache TTL continua servindo o último
     estado válido por uma janela curta e configurável (padrão sugerido:
     15 minutos); cada resposta degradada entra em `tb_legal_gate_audit`
     marcada como vinda do cache; esgotada a janela sem reconexão, tudo
     bloqueia. Queda de 2 minutos passa despercebida; queda de horas desliga
     o produto — correto nas duas pontas. "Falha de consulta" e "não há
     regra" continuam sendo coisas distintas: a segunda bloqueia na hora
     (decisão 104), sem janela nenhuma.

     **Duas amarras:**
     - O kill switch da decisão 107 **não participa da degradação** —
       `operational_state` tem TTL zero por desenho (plano §7); se não dá
       para consultá-lo, a jurisdição é tratada como suspensa. O atalho de
       emergência não pode depender de cache.
     - A janela degradada serve **apenas** chaves que já estavam em cache.
       Capacidade nunca consultada por esta instância não tem "último estado
       conhecido" — bloqueia, mesmo dentro da janela.

## Segurança de software

110. **O modelo de segurança do VGR é minimização em seis camadas, e o
     ativo número 1 é a correlação identidade ↔ denúncia.** Plano completo,
     modelo de ameaça e auditoria em `AI\docs\plans\plano-seguranca.md`.
     O que esta decisão fixa:

     1. **Hierarquia de ativos**: correlação identidade↔denúncia (risco de
        morte, decisão 40) > identidade de registrados > localização >
        integridade administrativa > instruções de pagamento. Investimento
        de segurança segue essa ordem, não a ordem de chegada das features.
     2. **Minimização como princípio reitor**: a defesa mais forte é não
        ter o dado. Campo identificável novo exige por quê, TTL e quem lê —
        declarados no PR. O que não foi coletado não pode vazar nem ser
        intimado.
     3. **Seis camadas** (SEC-1 minimização, SEC-2 borda, SEC-3 identidade,
        SEC-4 autorização — já construída, SEC-5 dado em repouso, SEC-6
        rastreabilidade), cada uma falhando fechada, independentes.
     4. **Regras permanentes de desenvolvimento** (bloqueantes em review):
        log nunca recebe senha/token/body/IP de denunciante/localização;
        SQL sempre parametrizado; endpoint novo nasce com `requirePrivilege`
        e, se couber risco legal, `requireCapability`; erro externo é
        `{ error, code }`; segredo só em env.
     5. **Três achados objetivos corrigidos na mesma sessão** (A1 log de
        body com senha em texto claro — crítico; A2 `JWT_SECRET ?? ''`
        aceitando tokens forjáveis — crítico; A3 Swagger público em
        produção). Correções em `app.ts`, `shared/config/env.ts`,
        `auth.middleware.ts`, `admin-login.service.ts`, `server.ts`.

     Segurança física e de servidor é assunto de implantação; as instruções
     que a implantação deve seguir estão no §6 do plano (TLS, secret
     manager, banco isolado, CORS real, retenção curta de log).

111. **A criptografia da decisão 44 é envelope encryption: DEK por registro,
     KEK fora do banco.** Fecha o item 1 da rodada 4. Cada registro sensível
     é cifrado com AES-256-GCM por uma chave de dado (DEK) própria; a DEK
     viaja cifrada junto do registro, protegida pela chave-mestra (KEK) que
     nunca toca o banco — `LEGAL_KEK` no env agora, secret manager na
     implantação (§6 do plano de segurança). Invasão do banco, sozinha,
     expõe lixo binário — que é exatamente o enunciado da decisão 44.

     **Escopo inicial**: `tb_accountability_log.ip_address` e `.metadata`
     (o ativo nº 1 da decisão 110). Campos futuros de Report/HelpOffer em
     categoria crítica (40) já nascem cifrados pelo mesmo utilitário —
     `shared/crypto/`, sem dependência de KMS externo.

     **Propriedades que o desenho fixa**:
     1. Rotação de KEK recifra apenas DEKs (colunas de bytes), nunca os
        dados — cada registro guarda a versão da KEK que o cifrou.
     2. Comprometimento de uma DEK expõe UM registro — corta-fogo por
        linha.
     3. GCM dá integridade junto: registro adulterado falha na decifra —
        importa num log que existe para responsabilizar (decisão 23).
     4. A decifra continua atrás do duplo controle da decisão 45: o
        utilitário é de `shared/`, mas o único caminho de leitura é o
        fluxo dual-control — nenhuma rota nova de leitura nasce disso.
     5. Boot de produção exige `LEGAL_KEK` presente (mesmo fail-fast da
        decisão 110/A2 para `JWT_SECRET`).

112. **Sessão administrativa: access token de 15 minutos + `session_version`
     em `tb_user`.** Fecha o item 2 da rodada 4. O token carrega a versão de
     sessão do usuário no momento do login; cada validação compara com o
     banco pelo mesmo cache de 60s do privilege-store — custo por request
     ~zero. Desativar usuário, trocar senha ou "derrubar sessões"
     incrementa a versão: toda sessão daquele usuário morre em ≤60s.

     O `JWT_EXPIRES_IN` default muda de 24h para 15m; o app renova
     silenciosamente via o fluxo "manter conectado" que a Fase 2 já
     construiu (re-login com credencial guardada em storage seguro — item 7
     da rodada), e sem "manter conectado" a sessão simplesmente expira em
     15 minutos de inatividade — comportamento correto para um painel que
     concede privilégios e decifra dado sensível.

     Refresh token rotativo com detecção de reuso fica **documentado como
     evolução** (quando houver instalação multi-servidor ou exigência de
     sessão longa sem credencial armazenada), não como dívida.

113. **Proteção por conta: atraso progressivo no login, código de recovery
     invalidado na 5ª falha — nunca bloqueio duro.** Fecha o item 3 da
     rodada 4. Login: a partir da 5ª falha consecutiva na mesma conta, cada
     tentativa espera exponencialmente mais (1s, 2s, 4s… teto 30s); o
     contador zera no sucesso. Recovery: 5 códigos errados invalidam o
     código — força bruta contra as 10⁶ combinações morre; só um novo
     pedido gera outro código. Contadores em colunas de `tb_user`
     (`failed_login_count`, `recovery_attempt_count`), sem tabela nova.

     **Por que bloqueio duro foi descartado, registrado para não voltar**:
     trancar a conta após N falhas transforma o e-mail público de um admin
     em arma de negação de serviço — e neste produto o admin pode estar no
     meio de um destrave de emergência da decisão 45 (risco iminente à
     vida). Atraso progressivo pune máquina sem trancar humano.

     A resposta ao chamador não muda em nada (mesmo 401 genérico, decisão
     110) — o atraso acontece server-side, sem revelar que a conta entrou
     em regime de proteção.

114. **Senha mínima de 12 + segundo fator TOTP obrigatório para todo
     usuário do painel.** Fecha o item 4 da rodada 4, na opção mais forte —
     coerente com o que este painel faz: concede privilégio, destrava dado
     de risco de vida (45), promove regra do Legal Gate (107).

     **Senha**: mínimo 12, máximo 72 (limite do bcrypt), sem regras de
     composição (NIST 800-63B — composição gera `Senha@123`; comprimento
     gera entropia), com recusa de lista local das ~1000 senhas mais
     comuns. Vale para senha nova (criação, troca, recovery); as
     existentes valem até a próxima troca — sem reset em massa.

     **2FA**: TOTP padrão (RFC 6238 — Google Authenticator e afins), sem
     SMS (SIM swap). Enrolamento obrigatório no primeiro login após a
     feature existir; login passa a ser senha + código. **Códigos de
     recuperação** (10, uso único, exibidos uma vez no enrolamento) são o
     caminho de "perdi o celular" — e o admin sem códigos e sem aparelho é
     destravado por outro admin com o duplo controle da decisão 45, nunca
     por atalho unilateral (decisão 70: sem superusuário).

     ⚠️ **Consequência de escopo assumida**: 2FA é uma fase de
     implementação própria (tabela de segredo TOTP + códigos, fluxo de
     enrolamento, telas no app, verificação no login), não um ajuste de
     DTO. Entra no plano de execução da rodada 4 como fase própria, depois
     das correções de menor esforço.

115. **Borda HTTP endurecida: helmet, CORS estrito, trust proxy.** Fecha o
     item 5 da rodada 4. helmet com HSTS/nosniff/frame-deny (CSP adiada até
     o painel ser servido pela API, se um dia for); `CORS_ORIGIN` vira
     lista explícita de origens — `*` só fora de produção, e produção sem
     origem configurada **recusa boot**, mesmo padrão fail-fast do
     `JWT_SECRET` (110/A2); `app.set('trust proxy', 1)` para o rate limit
     e o audit enxergarem o IP real atrás do proxy da implantação.

116. **Auditoria administrativa geral: `tb_admin_audit` append-only para
     todo CRUD do painel.** Fecha o item 6 da rodada 4 (SEC-6). Colunas:
     quem, ação, entidade, id, resumo antes→depois (JSON), IP, quando.
     Escrita fire-and-forget no padrão do audit do Legal Gate, chamada
     pelos services de usuários, privilégios, interfaces, módulos,
     risk-config e monetization-config. Sem rota de escrita/edição — só
     INSERT pelo código e leitura futura por tela própria. Hoje um
     privilégio concedido indevidamente não deixa rastro de quem o
     concedeu; isto fecha esse buraco.

117. **Token no cliente: secure storage no mobile; painel web mantém
     localStorage amparado pelo TTL curto.** Fecha o item 7 da rodada 4.
     Mobile: `flutter_secure_storage` (Keychain/Keystore) substitui
     SharedPreferences para o token quando "manter conectado" — cifrado
     pelo sistema, inacessível a outro app. Painel web: localStorage
     permanece; com o token de 15 minutos da decisão 112, roubo por XSS
     vale minutos — migração para cookie httpOnly fica registrada como
     opção futura, não como dívida (reescreveria o contrato de auth dos
     dois clientes contra um vetor já encolhido). Junto: o app ganha
     tratamento próprio para o **451 do Legal Gate** — tela de "bloqueado
     por decisão legal nesta jurisdição" com o motivo tipificado, nunca
     erro genérico.

118. **Dependências: `npm audit` manual obrigatório antes de release; no
     CI quando o CI existir.** Fecha o item 8 e a rodada 4 inteira.
     Checklist de release ganha `npm audit` (API) e `dart pub outdated`
     (app); lockfile sempre commitado; `engines` no package.json registra
     a versão mínima de Node. Quando o CI nascer (cross-ref: git hygiene
     do vgr-kit), `npm audit --audit-level=high` falha o build. PR
     automático de dependência fica para depois do CI — upgrade às cegas
     sem testes rodando não é higiene, é risco.

## Autenticação dos usuários do app

119. **Dois planos de autenticação, nunca cruzados — e e-mail/senha entra
     como método do app.** O painel (`tb_user`, decisões 110-118) e o app
     (`UserAccount`, decisões 4/31) são sistemas de autenticação separados:
     tabelas separadas, JWT com `aud` distinto (`admin` vs `app`) e
     rejeição cruzada nos middlewares — token de um plano é 401 no outro,
     por construção. Um vazamento ou fraqueza no plano do app nunca escala
     para o painel que decifra dado de risco de vida.

     **Métodos do app**: os da decisão 31 (Google, Apple, Facebook, OTP
     telefone/WhatsApp — item 1 da rodada 5 confirma o OTP) **mais
     e-mail/senha**, acrescentado por esta decisão. Anônimo continua sem
     autenticação nenhuma (decisões 32/35) — autenticar só é exigido
     quando a ação exige identidade (33/34).

     **Regras de segurança fixadas** (aplicam a decisão 110 ao caso):
     1. Token de provedor social é verificado **server-side** (assinatura
        pelas chaves públicas do provedor, `iss`, `aud`, `exp`, `nonce`) e
        **nunca armazenado** — troca-se pelo JWT próprio na hora.
     2. Minimização do perfil: guarda-se `sub` do provedor, e-mail, flag
        de e-mail-verificado e nome de exibição. Foto, grafo social,
        contatos e telefone do perfil **não entram no banco**.
     3. Uma conta, N provedores: tabela de vínculo
        (`tb_user_account_provider`), upsert idempotente (task 17). As
        regras de vínculo por e-mail são o item 2 da rodada 5.
     4. Senha de app (quando o método for e-mail/senha) usa bcrypt e as
        regras de log da 110; política e 2FA são o item 5 da rodada.
     5. O fluxo anônimo permanece sem token e sem conta — o rastro dele é
        o accountability log da decisão 23, não sessão.

120. **O app tem cinco métodos de login: Google, Apple, Facebook, OTP
     telefone/WhatsApp e e-mail/senha.** Fecha o item 1 da rodada 5,
     confirmando a decisão 31 e somando o método da 119. O OTP fica pelo
     motivo de inclusão: é o único método que não exige e-mail nem conta em
     big tech — e no público de denúncia comunitária no Brasil isso não é
     nicho. Risco de SIM swap assumido e contido pela 119: OTP autentica
     só o plano do app, nunca o painel. Custo de envio (SMS/WhatsApp) é
     operacional, não bloqueia o desenho.

121. **Vínculo de contas: automático apenas com e-mail verificado dos dois
     lados.** Fecha o item 2 da rodada 5. Auto-vínculo quando o provedor
     social afirma `email_verified` E a conta local já verificou o mesmo
     e-mail. Login social batendo em conta-senha não verificada → exige a
     senha antes de vincular (prova de posse). Sem verificação mútua →
     contas separadas com aviso. Regras acessórias fixadas junto:
     - E-mail de relay privado da Apple (`@privaterelay.appleid.com`)
       **nunca** auto-vincula — é alias por conta, não identidade.
     - Vínculo manual ("conectar outro login") sempre disponível dentro da
       conta autenticada, com re-autenticação recente (≤5 min).
     - Desvincular exige que reste ao menos um método utilizável — conta
       nunca fica órfã de login.
     - Troca de e-mail em qualquer dos lados zera a flag de verificado e
       repete o processo.

122. **Sessão do app: access de 30 minutos + refresh rotativo de 90 dias.**
     Fecha o item 3 da rodada 5. Refresh em secure storage (decisão 117),
     rotativo — cada uso emite um novo e invalida o anterior; **reuso de
     refresh antigo revoga a família inteira** (sinal clássico de roubo).
     `UserAccount` ganha `session_version` (mesmo mecanismo da 112):
     banir/desativar derruba todas as sessões em ≤60s. Resultado: usuário
     logado por meses, como um app deve ser; token vazado valendo minutos.
     Contraste deliberado com o painel (15 min secos): o painel concede
     privilégio e decifra dado de risco de vida; o app não — cada plano com
     a sessão do seu risco (decisão 119).

123. **"A denúncia nunca espera": verificação de e-mail (e qualquer outra
     exigência de identidade) acontece quando o caso escala, nunca no
     caminho da denúncia.** Fecha o item 4 da rodada 5 e eleva a escolha a
     princípio de produto, com o fluxo declarado pelo dono do produto:

     **Primeiro denuncia. Depois, se o caso escalar, identifica-se.**
     Cadastrar e denunciar sem recompensa: livre, sem código de e-mail no
     meio. Oferecer recompensa, reivindicar, virar respondedor: e-mail
     verificado (código de 6 dígitos, padrão do painel). Trote e falsa
     comunicação: responsabilização pelo log da decisão 23 (IP + arts.
     339/340 do CP, aviso da decisão 57) — proteção que não cobra atrito
     de quem denuncia de boa-fé.

     **Cenários de referência registrados** (calibram qualquer exigência
     futura de fricção):
     - *Cachorro perdido*: há tempo — fricção tolerável.
     - *Sumiço de criança em shopping ("apito na praia")*: o pai abre o
       app e denuncia EM SEGUNDOS; usuários próximos são alertados
       (decisões 2/7); criança localizada → caso encerra **sem
       identificação de nenhum ator** (decisões 32/35); não localizada →
       caso escala, autoridades entram, raio aumenta.
     - *Violência pública*: denúncia imediata, mesma lógica.
     - *Violência doméstica*: vítima denuncia depois da agressão;
       observador pode denunciar caso iminente, em curso ou passado — a
       hesitação do observador é exatamente o que o atrito zero protege.

     **Escalonamento progressivo como regra**: conforme o caso dura mais
     ou escala, o denunciante *opta* por fornecer mais dados e entrar em
     recompensa — e aí, e só aí, o processo de proteção dos usuários
     (identidade verificada, reserva, mediação) é acionado. Fricção é
     proporcional à consequência, nunca ao registro.

124. **Senha do app: mesma política do painel (mínimo 12, decisão 114);
     2FA TOTP opcional — e sem colisão com o cadastro social.** Fecha o
     item 5 e a rodada 5. A dúvida levantada ("colide com social?") tem
     resposta estrutural: **conta criada por login social não possui senha
     local** — a política de senha simplesmente não se aplica a ela. Ela
     só entra em cena quando o método e-mail/senha é criado: no cadastro
     direto por senha, ou quando um usuário social decide *adicionar*
     senha via vínculo manual (decisão 121). O 2FA TOTP é **da conta, não
     do método** — protege login por senha e pode ser exigido sobre login
     social também, se o usuário ativar. Oferecido com insistência a quem
     tem recompensa a receber; nunca obrigatório (matar adoção num app
     comunitário custa mais que o risco); papel police, se existir
     (decisão 12), nasce com 2FA compulsório.

125. **Visão registrada — profissionalização de helpers.** O dono do
     produto prevê que ajudar pode virar negócio (pessoas vivendo de
     resolver denúncias com recompensa). Documentada como visão, fora do
     MVP — mesma tratativa das decisões 11/12/43. Quando chegar a hora,
     toca: reputação (85), verificação reforçada do helper profissional
     (34), fiscal/tributário da recompensa recorrente (pendência nova na
     ocasião) e o RiskTier (o profissional não muda as regras das
     categorias críticas da decisão 40).

## Imagens (fecha a rodada 7, exceto o provedor pago)

126. **Storage de imagens em degraus — MVP sem custo, provedor pago só
     quando houver volume real.** Fecha parcialmente o item 1 da rodada 7.
     A trajetória é: **filesystem adapter** em dev/test (zero infra) →
     **MinIO self-hosted** no MVP (mesmo servidor da API; zero custo de
     licença, o custo é o disco que já existe) → **provedor S3-compatible
     pago** quando o produto estiver efetivamente rodando e gerando
     receita/volume. O MinIO no MVP é deliberado: expõe a mesma API S3 do
     degrau final, então o adapter que vai à produção é exercitado desde o
     primeiro dia — migrar é copiar objetos e trocar config, nunca
     reescrever (regra 2 do `plano-imagens.md`).

     **A escolha do provedor pago continua aberta** (é comercial, padrão
     das decisões 59/rodada 6). Finalistas e critérios registrados no §3
     do plano: custo por GB armazenado E trafegado (toda visualização
     passa pela API — egress pesa), jurisdição do byte, presença no
     Brasil. Nota que reequilibra a comparação: como `evidence` é
     ciphertext (cifra envelope, chave nunca sai da API), o risco
     jurisdicional do storage é reduzido — o provedor guarda ruído.

127. **Avatar adiado — fora do MVP.** Fecha o item 2. A classe `avatar`
     fica especificada no plano e **desligada por config**; ligar depois é
     aditivo. A regra 2 da decisão 119 (foto de perfil social nunca entra
     no banco) permanece intocada. Cadastro no MVP não tem imagem nenhuma.

128. **Blur-por-default no feed para categorias críticas.** Fecha o item 3.
     Nas categorias da decisão 40, a miniatura aparece borrada e o usuário
     toca para revelar. O borrão é gerado no ingest como derivado próprio
     (o thumbnail nítido nunca chega ao cliente para "desborrar").

129. **Limites de upload.** Fecha o item 4 com os números recomendados:
     **10 imagens por denúncia, 10 MB por arquivo** antes da normalização;
     entrada aceita jpeg/png/webp/heic (validados por magic bytes), saída
     normalizada em formato único. Números vivem em config, não em código.

130. **Metadados da foto (EXIF) são escolha do denunciante na captura,
     por foto — default é descartar.** Fecha o item 5, revisando a
     recomendação original (descarte sempre): no momento de anexar, o app
     oferece a opção **"manter dados probatórios da foto"**, com aviso
     claro do que esses dados revelam (onde a foto foi tirada, quando e
     com qual aparelho). Regras fixadas:
     - **Default = descartar.** Silêncio protege; manter é ato explícito.
     - Escolha é **por foto**, registrada com a versão do texto de aviso
       exibido (padrão da decisão 86).
     - Se mantiver: o **original é preservado cifrado** como evidência,
       junto do normalizado. O que circula no app/feed é **sempre** o
       normalizado sem EXIF — o original só é acessível pelo painel com
       privilégio e leitura auditada (decisão 116), para uso probatório.
     - Em denúncia **anônima**, o aviso é reforçado: os dados da foto
       podem revelar onde o denunciante estava (conflita com o anonimato
       que ele próprio escolheu — decisão 32). A opção continua existindo;
       a decisão é dele, informada.

131. **Retenção de evidência: 90 dias após a resolução como régua geral;
     caso escalado a autoridade congela.** Fecha o item 6. Estende a
     mesma janela da decisão 25 (menores) para toda evidência de caso
     resolvido, e amarra no mecanismo de dado congelado do Legal Gate
     (item 6 da rodada 2): caso nas mãos de autoridade não expira até
     desfecho. Apagamento é crypto-shredding (§7 do plano) — vale
     inclusive para backups.

132. **Vídeo e áudio ficam fora até decisão própria.** Fecha o item 7,
     confirmando a recomendação (padrão das decisões 11/12/43): mudam
     ordem de grandeza de custo, pipeline (transcoding) e risco de
     moderação. O port `BlobStore` os recebe no futuro sem retrabalho.

## Design system do app

133. **Nenhum widget do Flutter é usado diretamente numa tela — tudo é
     encapsulado em widget da casa com prefixo `Vgr`, em
     `packages/vgr_widgets`.** Mesma regra do setes-app (decisão 11 dele,
     prefixo `Setes`), trazida para este projeto. Objetivo: **trocar um
     widget obsoleto ou sem manutenção sem alterar o sistema inteiro** —
     muda uma implementação num arquivo, e as centenas de chamadas ficam
     onde estão.

     **Widget × componente**: no Flutter são o mesmo conceito; "componente"
     é o termo genérico, "widget" é a materialização. Termo oficial aqui:
     **widget** (mesma convenção da decisão 8 do setes).

     **Escopo**: telas e código de apresentação de `apps/*/lib` e
     `packages/core/lib`. Isento: o próprio `vgr_widgets` (encapsular é a
     função dele) e os testes. Peças estruturais que não são widget visual
     — `MaterialApp`, `Navigator`, `Theme`, `BlocBuilder` — ficam fora.

     **A regra é verificada por teste**, não por combinação:
     `apps/admin/test/design_system_guard_test.dart` falha o build listando
     arquivo e linha de cada violação. Isso não é zelo excessivo: a regra
     já estava escrita no `pubspec.yaml` do `vgr_widgets` desde o primeiro
     dia e mesmo assim havia **~350 usos diretos** de widget cru, porque
     nada conferia. Regra sem verificação vira sugestão.

     **Consequência nos testes**: teste afirma sobre o widget da casa
     (`tester.widget<VgrIconButton>`), nunca sobre o interno do Flutter —
     senão quebraria a cada troca de implementação, que é exatamente o
     acoplamento que esta decisão remove.

     Padrão documentado em `app/docs/adr/DESIGN-SYSTEM.md`.

## ⚠️ Pendências (rodada 1 — controles administrativos)

Nenhuma. Itens 1–4 → decisões 72–75; item 5 → decisão 80; item 3 (erro por
campo) → decisão 83; item 2 (`kind`) → decisão 93. **Rodada 1 encerrada.**

## ⚠️ Pendências (rodada 2 — Legal Gate)

Diretrizes nas decisões 76–79. Decididos em 2026-08-03: item 1 → **103**,
item 2 → **104**, item 3 → **105**, item 8 → **106** (escopo L0+L1),
item 4 → **107**, item 5 → **108**, item 9 → **109**.

**Código do Legal Gate (L0+L1) está DESBLOQUEADO** — todos os itens que o
travavam foram decididos. **Rodada 2 fechada por completo em 2026-08-20**
(decisões 143–146); só resta a escolha comercial do provedor da L2 (item 7,
mesmo formato de pendência do PSP e do OTP — não é arquitetura em aberto).

1. ~~**Granularidade do gate.**~~ — RESOLVIDO pela **decisão 103**:
   capacidade, com convenção `domínio.ação[.qualificador]`, desconhecida
   bloqueia e catalogada sem chamador é dívida.
2. ~~**Default de jurisdição real sem regra ativa.**~~ — RESOLVIDO pela
   **decisão 104**: fail-closed.
3. ~~**De onde vem a jurisdição aplicável.**~~ — RESOLVIDO pela **decisão
   105**: a da instalação, com a divergência eliminada por construção
   (cada instalação atende só quem está no seu país).
4. ~~**Quem ativa uma regra.**~~ — RESOLVIDO pela **decisão 107**:
   privilégio dedicado + duplo controle; kill switch desliga com um,
   religa com dois.
5. ~~**Regras expiram?**~~ — RESOLVIDO pela **decisão 108**: sim, 180 dias
   por padrão, sem isenção para regra confirmada por advogado.
6. ~~**Dado já coletado quando uma capacidade passa a bloqueada.**~~ —
   RESOLVIDO pela **decisão 145**: congela a leitura pela aplicação, nunca
   apaga por causa do bloqueio; mecanismo distinto do `frozen` da 141;
   sem onde se aplicar até o primeiro cabeamento real.
7. **O que se registra de cada avaliação de IA.** Recomendado: **modelo,
   hash do prompt, veredito, confiança, dispositivos citados e perguntas em
   aberto**. O custo é uma tabela; o retorno é conseguir mostrar *como* se
   chegou à conclusão. Alternativa: só o veredito. Critério de escolha do
   provedor e desenho do port fechados pela **decisão 144**; falta só a
   escolha comercial do provedor concreto.
8. ~~**Escopo imediato.**~~ — RESOLVIDO pela **decisão 106**: L0+L1 juntas,
   migração 022.
9. ~~**O que fazer quando a consulta ao gate falha?**~~ — RESOLVIDO pela
   **decisão 109**: último estado conhecido por janela limitada, kill
   switch fora da degradação.
10. ~~**Como se controla que o usuário está no país da instalação?**~~ —
    RESOLVIDO pela **decisão 146**: point-in-polygon local (dataset
    estático de fronteiras, ex. Natural Earth), sem provedor externo —
    coerente com a 135 (posição nunca sai da API). Fronteira cruzada não
    invalida caso já em andamento, só afeta criação de ação nova.

## ⚠️ Pendências (rodada 3 — trilho de pagamento)

Diretriz registrada na decisão 81. Decididos em 2026-08-03: item 1 (custódia)
→ **84**, item 6 (garantia) → **85**, item 8 (categoria crítica) → **86**,
mecanismo de reserva → **87**, item 11 (quem escolhe) → **88**, item 9
(expiração) → **89**. O item 5 foi retirado por ser pergunta indevida.

Depois disso: item 2 → **91**, item 14 → **92** e **102**, item 15 → **94**,
item 16 → **95**, item 3 → **96**, item 4 → **97**, item 12 → **98**,
item 10 → **99**. A decisão 95 (só Pix) revisou 87, 88, 89, 90, 94 e 102.

Item 7 → **101**, e a decisão 100 consolidou o contrato funcional da reserva.

**Pendências desta rodada: nenhuma.** O item 17 não é decisão, é fato a apurar
com o PSP — junto com a pergunta de titularidade da decisão 95, que é
bloqueante. Ambos estão no checklist
`AI\docs\plans\plano-psp-requisitos.md` (D1 e B1).

1. ~~**Modelo de custódia.**~~ — RESOLVIDO pela **decisão 84**: custódia
   zero, split pelo PSP. Escrow em nome do VGR e carteira interna
   descartados.
2. ~~**Quem contrata o PSP e aparece na transação.**~~ — RESOLVIDO pela
   **decisão 91**: VGR como facilitador de marketplace.
3. ~~**Um PSP global ou um por país.**~~ — RESOLVIDO pela **decisão 96**:
   um adapter por jurisdição, atrás da porta `PaymentRail`.
4. ~~**Onde não há PSP contratado.**~~ — RESOLVIDO pela **decisão 97**:
   bloqueia só `reward.monetary`; o resto do produto funciona.
5. ~~**Colisão com as decisões 40/42 — helper que não pode se
   identificar.**~~ **RETIRADA — pergunta indevida.** A colisão não existe:
   a decisão 60 já havia estabelecido que "identificação proibida" é
   perante outros usuários, não perante a plataforma, e por isso o KYC do
   PSP nunca foi obstáculo. Fechada em definitivo pela decisão 82
   (dinheiro via Pix/transferência, identidade só no plano administrativo,
   voucher proibido).
6. ~~**Como garantir o pagamento sem custódia?**~~ — RESOLVIDO pela
   **decisão 85**: garantia é escolha do denunciante (pré-autorização
   opcional) e vira selo visível na denúncia; cada lado assume o seu risco.
7. ~~**Texto dos selos e das opções de oferta.**~~ — RESOLVIDO pela
   **decisão 101**: selo binário, "recompensa garantida" ou ausência de
   selo, sem rótulo negativo.
8. ~~**Recompensa sem reserva nas categorias críticas?**~~ — RESOLVIDO pela
   **decisão 86**: permitida, com ciência explícita e registrada do helper
   antes de ele se oferecer.
9. ~~**Quem é avisado quando a reserva expira?**~~ —
   RESOLVIDO pela **decisão 89**: denunciante avisado antes (renovação em um
   toque), helpers vinculados avisados ao expirar com a informação da
   decisão 86 — informa, não desvincula, não bloqueia.
10. ~~**Gatilho da integração própria.**~~ — RESOLVIDO pela **decisão 99**:
   autorização do BACEN (ou equivalente) + promoção por duplo controle, sem
   relaxar as proibições de arquitetura da decisão 84.
11. ~~**Quem define a faixa entre pré-autorização e retenção no PSP?**~~ —
   RESOLVIDO pela **decisão 88**: o denunciante escolhe, numa pergunta só de
   três opções. Sem cadastro administrativo de faixa.
12. ~~**Mediação vira capacidade do Legal Gate?**~~ — RESOLVIDO pela
   **decisão 98**: sim, `reward.mediation`, e `reward.monetary` passa a
   depender dela na mesma jurisdição.
13. ~~**Como a API executa trabalho agendado?**~~ — RESOLVIDO pela
   **decisão 90**: `node-cron` in-process, registrado em
   `src/gateway/scheduler.ts`, com guardas de ambiente e trava de instância.
14. ~~**Quem absorve o chargeback?**~~ — RESOLVIDO pelas decisões **92**
   (aviso de que recompensa liberada não retorna, como prova na contestação)
   e **102** (repasse ao helper fora das críticas; VGR absorve nas críticas).
15. ~~**Prazo entre resolução e repasse ao helper**~~ — RESOLVIDO pela
   **decisão 94**: repasse só após a janela de contestação do instrumento.
16. ~~**O prazo de repasse varia por instrumento?**~~ — RESOLVIDO pela
   **decisão 95** eliminando a pergunta: só existe um instrumento, Pix.
17. ⚠️ **NOVA — a retenção de Pix no PSP tem prazo máximo?** Criada pela
   decisão 95, e decide o destino das decisões 89 e 90. Se o PSP limita por
   quanto tempo pode segurar um valor retido, o vencimento volta a existir
   (em outra escala) e a decisão 89 se aplica com ajuste de prazos; se não
   limita, a reserva dura até a resolução e as decisões 89/90 podem ser
   arquivadas. **Não é escolha nossa — é fato a apurar** na pesquisa da
   decisão 59, junto com a pergunta de titularidade. Fica registrada aqui
   para não se perder enquanto o PSP não é escolhido.

## ⚠️ Pendências (rodada 4 — segurança de software)

Diretriz registrada na decisão 110; auditoria completa no
`plano-seguranca.md` §3. **RODADA FECHADA em 2026-08-03** — os oito itens
viraram as decisões 111–118. Plano de execução em fases no
`plano-seguranca.md` §8; nada codado ainda (decisão 38: Valdo libera fase a
fase).

1. ~~**Como implementar a criptografia em repouso da decisão 44.**~~ —
   RESOLVIDO pela **decisão 111**: envelope encryption, DEK por registro,
   KEK fora do banco, escopo inicial no log de responsabilização.
2. ~~**Sessão administrativa: TTL e revogação.**~~ — RESOLVIDO pela
   **decisão 112**: 15 min + `session_version`, revogação em ≤60s.
3. ~~**Lockout por conta.**~~ — RESOLVIDO pela **decisão 113**: atraso
   progressivo, código invalidado na 5ª falha, bloqueio duro descartado.
4. ~~**Política de senha.**~~ — RESOLVIDO pela **decisão 114**: mínimo 12
   sem composição + lista de proibidas, E 2FA TOTP obrigatório (opção mais
   forte; 2FA vira fase própria de implementação).
5. ~~**Headers e CORS.**~~ — RESOLVIDO pela **decisão 115**: helmet + CORS
   estrito com fail-fast + trust proxy.
6. ~~**Auditoria de ações administrativas.**~~ — RESOLVIDO pela **decisão
   116**: `tb_admin_audit` append-only para todo CRUD do painel.
7. ~~**Armazenamento do token no cliente.**~~ — RESOLVIDO pela **decisão
   117**: secure storage no mobile, web com TTL curto; tela própria para o
   451.
8. ~~**Higiene de dependências.**~~ — RESOLVIDO pela **decisão 118**:
   audit manual no release agora, no CI quando o CI existir.

## ⚠️ Pendências (rodada 5 — autenticação dos usuários do app)

Diretriz na decisão 119; plano em `plano-auth-usuarios.md`. **RODADA
FECHADA em 2026-08-03** — itens 1–5 viraram as decisões 120–124 (+125,
visão registrada junto). Nada codado; implementação entra na fila atrás
das fases S1–S6 da segurança (ou junto, quando tocarem os mesmos arquivos).

1. ~~**OTP telefone/WhatsApp continua no conjunto?**~~ — RESOLVIDO pela
   **decisão 120**: continua; cinco métodos no total.
2. ~~**Vínculo de contas com o mesmo e-mail.**~~ — RESOLVIDO pela **decisão
   121**: verificado dos dois lados; relay da Apple nunca auto-vincula.
3. ~~**Sessão do app.**~~ — RESOLVIDO pela **decisão 122**: access 30min +
   refresh rotativo 90d com detecção de reuso; session_version na conta.
4. ~~**Verificação de e-mail no cadastro por senha.**~~ — RESOLVIDO pela
   **decisão 123**: "a denúncia nunca espera" — verificação quando o caso
   escala, com cenários de referência registrados.
5. ~~**Política de senha e 2FA do usuário do app.**~~ — RESOLVIDO pela
   **decisão 124**: min 12 igual painel, TOTP opcional da conta; sem
   colisão com social (conta social não tem senha local).

## ⚠️ Pendências (rodada 6 — provedores de autenticação do app)

Nasceram ao implementar as decisões 119–124. Nenhuma bloqueia o que já
está construído (senha, sessão, vínculo, gate de verificação): o serviço
aceita uma identidade **já verificada**, então plugar verificador é
aditivo. O que falta é escolha de fornecedor, não desenho.

1. ⚠️ **Qual provedor de envio para o OTP de telefone/WhatsApp**
   (decisão 120). Mesma natureza da pendência do PSP (decisão 59): é
   escolha comercial, não técnica. Enquanto não houver, o método OTP não
   existe na prática — os outros quatro funcionam. Critérios a levar:
   custo por mensagem, entrega em WhatsApp além de SMS, presença no
   Brasil, e API de verificação (ou só envio, com o código sendo nosso).
2. ~~**Verificação de e-mail: usar o mailer que já existe?**~~ —
   RESOLVIDO pela **decisão 151**: reaproveita `shared/mailer`, TTL e
   contador próprios do app.
3. ~~**Adapters de provedor social — construir agora ou junto da
   primeira tela de login do app?**~~ — RESOLVIDO pela **decisão 152**:
   adiados até haver credencial OAuth real; o app ganha a tela de
   e-mail+senha agora.

## ⚠️ Pendências (rodada 7 — imagens)

Itens 2–7 → decisões 127–132. Item 1 parcialmente fechado pela decisão 126
(degraus: filesystem → MinIO self-host no MVP → provedor pago). **Resta um
único aberto**:

1. ⚠️ **Qual provedor S3-compatible pago no degrau final** (decisão 126) —
   escolha comercial que só precisa acontecer quando o produto estiver
   rodando com volume real; até lá o MinIO cobre tudo. Finalistas com
   preços de referência e critérios no §3 do `plano-imagens.md`
   (verificar preços na contratação).

## Denúncia (rodada 8 — primeira leva)

134. **Anexo anônimo de mídia: o `publicId` é o segredo portador.** Fecha o
     item 2 da rodada 8. UUID v4 (122 bits de aleatoriedade) é
     inadivinhável na prática; quem o apresenta pode anexá-lo a uma
     denúncia — uma única vez (o attach consome o estado pending). Mídia
     enviada por conta autenticada só anexa pela mesma conta; todo attach
     anônimo registra no accountability log (decisão 23).

135. **O feed público serve localização DEGRADADA por tier — a posição
     exata nunca sai da API.** Fecha o item 3. Em violência doméstica a
     posição exata da denúncia é a casa da vítima. Feed anônimo/público:
     posição arredondada (tier baixo ~rua; alto/crítico ~bairro),
     distância aproximada, categoria e tempo relativo; nunca reporterId,
     nunca contagem/timestamps de ofertas em tier alto (decisões 40/41/60).
     A posição exata existe só para participantes conforme visibilidade
     (50) e para autoridade via fluxos auditados.

136. **Mídia órfã expira em 48h.** Fecha o item 4. Pending nunca anexada
     entra no job de expiração existente (decisão 131) e é
     crypto-shredded. Config, não constante.

137. **Idempotência do submit: UUID gerado no app, um por denúncia.**
     Fecha o item 6. Coluna única em tb_report; replay da fila offline
     (decisão 28) devolve o MESMO reportId com 200 — nunca duplica, nunca
     409. É o que torna a decisão 123 segura na prática.

138. **`report.media` é capacidade do Legal Gate.** Fecha o item 7. Nasce
     em PENDING_WIRING e é cabeada no R4 (a partição do catálogo obriga a
     remoção na hora certa).

139. **Texto do aviso EXIF v1 aprovado.** Fecha o item 8. O rascunho do §5
     do plano-denuncia.md vira `exif-warning/v1` (com a variante reforçada
     do fluxo anônimo), gravado por foto no padrão da decisão 86.

140. **Taxonomia: dois eixos, ambos OBRIGATÓRIOS, semente livre, lista em
     código.** Fecha o item 1 da rodada 8 (executa a decisão 3 no modelo
     de dados):
     - (a) O MVP tem categoria × objeto/sujeito.
     - (b) **Objeto/sujeito é obrigatório** (o dono contrariou a
       recomendação de opcional). Guarda da decisão 123 incorporada: a
       lista de objetos inclui uma opção genérica ("other") de um toque —
       campo obrigatório nunca pode travar a denúncia de segundos do
       "apito na praia".
     - (c) **Os ícones herdados são só ponto de partida e referência** —
       a semente canônica é definida na implementação com liberdade
       (nomes em inglês, decisão 17; rótulos traduzidos no app; ícones
       aproveitados onde couberem). Tag livre da decisão 9 continua por
       cima para categoria.
     - (d) As listas vivem em CÓDIGO (value objects) no MVP; registro
       administrável por tela é evolução futura — mesma trajetória do
       risk-config.

141. **Congelamento: humano congela, humano descongela, caso inteiro —
     "não podemos destruir provas".** Fecha o item 5:
     - (a) Congelar é ação humana no painel (recurso kind 'R' próprio),
       com motivo obrigatório (ex. nº do ofício/processo) e auditoria.
       Nunca automático no MVP.
     - (b) Escopo: **o caso inteiro** — report + timeline + todas as
       mídias, num ato só.
     - (c) Princípio declarado pelo dono: destruição de prova é
       inaceitável — caso escalado a autoridade DEVE estar congelado
       antes de qualquer expiração.
     - (d) Descongelar também é humano pelo painel. Acessórios da
       recomendação incorporados por coerência com (c): descongelamento
       por **dual-control** (2 aprovadores distintos, padrão da 107 —
       descongelar é o ato que reabilita a destruição) e o prazo de
       retenção **recomeça** no descongelamento (90 dias contados dali).

142. **Painel nesta frente: só a tela mínima do congelamento.** Fecha o
     item 9 pela alternativa (c): busca administrativa completa, fila de
     moderação e estatísticas viram **frente própria depois do A3**, tendo
     como semente a única tela que entra agora — buscar caso por id +
     congelar/descongelar com motivo (consequência operacional da 141a/d).

     **Rodada 8 ZERADA** (decisões 134-142).

## ⚠️ Pendências (rodada 8 — denúncia)

Abertas em 2026-08-03 junto com o `plano-denuncia.md` (abertura da frente
central: Report + feed + HelpOffer + ciclo de vida + M2 de imagens; emendas
E1-E8 propostas à tactical design, que é anterior ao Legal Gate, aos dois
planos de auth, à mídia e à decisão 123). Nada codado.

**RODADA ZERADA em 2026-08-03**: itens 2/3/4/6/7/8 → decisões 134-139;
itens 1/5/9 (respondidos por sub-item após explicação ampliada) → decisões
140-142. O texto ampliado dos itens 1/5/9 abaixo fica como registro do
raciocínio apresentado.

1. ⚠️ **Taxonomia — o que está em jogo.** A decisão 3 classifica a
   denúncia por DOIS eixos: **categoria** (o que aconteceu: assalto,
   agressão, desaparecimento...) × **objeto/sujeito** (sobre quem/o quê:
   criança, adulto, animal, veículo, arma...). Os ícones herdados do app
   antigo existem para os dois eixos (`AI/docs/categoria` e
   `AI/docs/Objetos`). A spec, porém, só implementou o primeiro eixo
   (`category | freeTag`) — o objeto aparece de contrabando, como
   "SubjectTag=Child" na regra de retenção da decisão 25.

   **Por que decidir agora e não depois**: (a) a retenção de menores (25)
   precisa saber que o sujeito é criança — sem o eixo, vira interpretação
   de tag livre, frágil demais para uma regra legal; (b) risco e raio
   podem variar pela combinação (criança desaparecida ≠ adulto
   desaparecido); (c) acrescentar o eixo depois exige migração e
   reclassificação de denúncias reais já registradas.

   **Sub-decisões** (recomendação entre parênteses):
   a) O MVP tem os dois eixos? (**sim**)
   b) Objeto/sujeito é obrigatório? (**opcional** — o formulário da
      categoria (47) pode exigi-lo onde fizer sentido, ex. desaparecido)
   c) Semente das listas? (**união spec + ícones** para categoria — inclui
      "kidnapping" dos ícones e mantém "traffic"/"vandalism" da spec;
      objetos = lista de `AI/docs/Objetos`; nomes canônicos em inglês,
      decisão 17; rótulos traduzidos no app)
   d) Lista curada vive em código (VO, como a spec) ou em tela
      administrável? (**código no MVP**; tela admin é evolução natural,
      mesma trajetória do risk-config)
   e) Tag livre continua por cima para o que não se encaixa (decisão 9 —
      sem mudança).
2. **Anexo anônimo de mídia: o `publicId` vale como segredo portador?**
   Denunciante anônimo não tem conta para provar posse. Recomendação:
   aceitar — UUID v4 (122 bits) é inadivinhável; regras: anexo consome o
   pending (um attach só), mídia de conta só anexa pela mesma conta, e
   attach registra no accountability log (23).
3. **O que o feed público expõe — e com que precisão de localização?** O
   feed é visível sem conta (2/7/32); em violência doméstica a posição
   exata da denúncia é a casa da vítima. Recomendação: posição **exata
   nunca sai da API** — feed serve posição degradada por tier (baixo:
   ~rua; alto/crítico: ~bairro + raio), distância aproximada, categoria,
   tempo relativo; nunca reporterId, nunca contagem de ofertas em tier
   alto (41/60).
4. **TTL de mídia órfã**: pending nunca anexada expira e vira
   crypto-shredding no job existente. Recomendação: **48h**.
5. **Congelamento — o que está em jogo.** Quando um caso escala para
   autoridade (polícia investigando, ofício, intimação), os dados dele
   NÃO podem mais expirar: apagar prova em investigação é gravíssimo. Mas
   a retenção (131) apaga tudo 90 dias após a resolução. Sem um mecanismo
   de congelamento, ou o job destrói prova no dia 91, ou alguém desliga a
   retenção inteira "por precaução" — e a promessa de minimização (110)
   morre. A coluna `frozen` já existe na mídia e o job já a respeita; o
   que não existe é **quem liga e desliga** essa chave. (Conversa com o
   item 6 da rodada 2 do Legal Gate — "dado congelado quando capacidade
   fecha" — mesmo mecanismo, outro gatilho.)

   **Sub-decisões** (recomendação entre parênteses):
   a) Quem congela? (**humano no painel**, recurso kind 'R' próprio, com
      motivo obrigatório — ex. número do ofício/processo — e auditoria;
      nunca automático no MVP, não há integração com autoridade)
   b) Escopo? (**o caso inteiro**: report + timeline + todas as mídias —
      congelar só a mídia deixaria o texto da denúncia expirar)
   c) Descongelar exige mais que congelar? (**sim — dual-control**:
      congela com 1, descongela com 2, análogo ao kill switch da 107;
      descongelar é o ato que destrói prova)
   d) Efeito ao descongelar? (**o prazo recomeça**: 90 dias contados do
      descongelamento, nunca "expirou ontem enquanto estava congelado")
6. **Idempotência da fila offline (28/123)**: o app reenvia quando a rede
   volta; sem chave, retry = denúncia duplicada. Recomendação: UUID
   gerado no app por denúncia, coluna única em tb_report; replay devolve
   o mesmo reportId (200, não 409).
7. **`report.media` entra como capacidade do Legal Gate?** Anexar imagem
   tem risco jurídico que varia por país e o mecanismo já existe.
   Recomendação: sim — nasce em PENDING_WIRING e é cabeada no R4.
8. **Texto v1 do aviso EXIF (130)**: o mecanismo exige a versão do texto;
   o texto é de produto/jurídico e ainda não existe. Sem ele a opção
   "manter dados probatórios" não aparece no app (A1). Proposta de
   rascunho no plano para você aprovar/editar.
9. **Painel — o que está em jogo.** A frente da denúncia poderia puxar
   para o painel: busca de denúncias, visualização completa, moderação
   (bloquear mídia/denúncia), congelamento, estatísticas. Cada tela
   dessas custa caro (grid + i18n + privilégios + testes — a frente de
   controles administrativos provou), e moderação já é frente própria
   declarada. Se tudo entrar, a frente central dobra de tamanho **antes
   de o app denunciar existir** — e o app é o produto.

   **Sub-decisões** (recomendação entre parênteses):
   a) Telas novas de painel nesta frente? (**nenhuma por padrão** — o
      operacional mínimo já existe: leitura auditada de mídia (M3) e
      Legal Gate)
   b) Exceção: se o item 5 fechar como "congela pelo painel", entra UMA
      tela mínima — buscar caso por id + congelar/descongelar com motivo.
      (**sim, só essa** — sem ela o congelamento não é acionável)
   c) Busca administrativa completa, fila de moderação, estatísticas?
      (**frente própria depois do A3** — a tela mínima do congelamento é
      a semente natural dela)

## Encapsulamento de provedores externos (API) e provedor da L2

143. **Nenhum SDK de provedor externo é chamado direto de dentro de um
     módulo de domínio — sempre por um *port* (interface) em `shared/`,
     com a implementação concreta trocável por configuração.** Formaliza
     para a API o que já era prática (não regra escrita): `BlobStore`
     (decisão 126, `shared/storage/blob-store.ts`, `fs`/`s3` por
     `BLOB_STORE`) e `PaymentRail` (decisão 96) já seguem esta forma.
     Mesmo motivo da decisão 133 no app (widget Flutter cru → `Vgr*`):
     **trocar um provedor obsoleto, descontinuado ou substituído por um
     melhor é mudança de config + uma classe nova, nunca reescrita
     espalhada por módulos.**

     **Escopo**: qualquer serviço externo com SDK/API próprio — storage
     (já feito), pagamento, avaliação por IA (L2, decisão 144), envio de
     OTP e verificação social (rodada 6, ainda bloqueada na escolha do
     provedor), e-mail. Módulo de domínio importa a interface do port;
     nunca o SDK do provedor, nunca um tipo do provedor (bucket, região,
     nome de modelo, formato de payload) vazando para entidade/DTO/tabela
     — mesma regra de isolamento que o `BlobStore` já documenta em
     comentário.

     **Consequência estrutural**: o port vive em `shared/legal/`,
     `shared/storage/`, etc. (nunca dentro de um módulo — regra do
     `ARCHITECTURE.md` que proíbe módulo importar módulo, já usada pelo
     próprio Legal Gate); a implementação concreta é selecionada uma vez,
     memoizada, com função de reset para teste — padrão de
     `blobStore()`/`resetBlobStoreForTests()`.

     **Não coberto por esta decisão**: widgets do app (já é a 133) e
     bibliotecas puramente internas (dartz, bloc) — a regra é sobre
     *provedor externo*, não sobre toda dependência.

144. **Critério de escolha do provedor de IA da L2: grounding/citação
     verificável pesa mais que preço bruto por token.** Fecha a pergunta
     "qual o mais em conta" levantada para a L2 com a resposta errada
     descartada antes de decidir o modelo. Preço por token varia ~50x no
     mercado (de ~$0,15/$0,60 por milhão em modelos de extração em massa a
     ~$3/$15 em modelos de uso geral, ago/2026), mas dois fatos tornam essa
     variável irrelevante para a L2:

     - **Volume é baixíssimo.** A avaliação roda por `capability ×
       jurisdiction` (catálogo de dezenas de itens, plano-legal-gate.md
       §5), em lote, reexecutada ocasionalmente — nunca por requisição de
       usuário. O custo total de qualquer opção do mercado é irrisório
       nesse volume; a diferença entre a mais barata e uma boa opção não
       aparece na fatura.
     - **O erro caro aqui não é custo, é citação inventada.** A avaliação
       da IA não é parecer e não decide sozinha (§2 do plano) — mas
       alimenta a promoção humana a regra ativa (decisão 103/L3). Um
       modelo sem busca (grounding) cita dispositivo de lei "de memória",
       e memória de modelo erra citação com frequência maior que o
       aceitável quando a citação vai para uma tela que um gestor lê para
       decidir. Modelos otimizados para extração em massa e preço mínimo
       tipicamente não têm busca embutida.

     **Critério fechado, nesta ordem**: (1) busca web nativa/grounding
     disponível na chamada, para citar legislação vigente e não só
     recordada do treino; (2) aderência confiável a schema JSON
     estruturado (verdict, confidence, citations, open_questions — mesmo
     shape de `tb_legal_assessment`, plano-legal-gate.md §6); (3) preço,
     como critério de desempate entre opções que já passam em (1) e (2) —
     nunca como critério principal. Provedor concreto (qual API, qual
     modelo) não é decisão de arquitetura e fica em aberto para escolha
     comercial quando a L2 entrar em execução — mesmo formato de pendência
     do PSP (59) e do OTP (rodada 6): a arquitetura não espera a escolha.

     **Consequência estrutural**: port `LegalAssessmentProvider` em
     `shared/legal/`, seguindo a decisão 143 — método
     `assess(capability, jurisdiction) → { verdict, confidence, citations,
     openQuestions }`, sem nenhum tipo do provedor escolhido vazando para
     `tb_legal_assessment` ou para o restante da L2. A implementação
     concreta nasce quando o provedor for escolhido; até lá o port pode
     existir vazio (mesma situação do `PaymentRail`, decisão 96 — a
     interface não depende do fornecedor para ser definida).

## Legal Gate — pendências 6 e 10 fechadas

145. **Dado já coletado sob capacidade que passa a bloqueada: congela a
     leitura pela aplicação, nunca apaga por causa do bloqueio.** Fecha o
     item 6 da rodada 2. O gate já cobre a ponta de escrita — nenhuma ação
     nova acontece sob capacidade `blocked`/`restricted` (decisão 104); a
     pendência era só sobre o dado que já existia sob a regra anterior.
     Apagar entraria em conflito com a retenção (decisão 25/131) e com
     dever de guarda; manter 100% acessível anularia o efeito do bloqueio
     na prática.

     **Mecanismo distinto do `frozen` da decisão 141** — mesmo nome
     tentador, gatilhos e efeitos diferentes: 141 é ato manual de admin
     que **trava expiração** para preservar prova numa investigação; este
     é efeito **automático** de leitura quando uma regra do Legal Gate
     muda de estado, sem tocar no job de retenção. Nomear no código como
     `legal-blocked`, não `frozen`, para não confundir os dois.

     **Não tem onde se aplicar hoje** — nenhuma capacidade real está
     cabeada (tudo em `PENDING_WIRING`, decisão 103). O comportamento
     entra junto com o primeiro cabeamento real que expuser leitura de
     dado sob capacidade bloqueável (ex. R4 da denúncia, decisão 138), não
     antes.

146. **Controle de "estar no país": point-in-polygon local, sem provedor
     externo — a posição não sai da API para checar fronteira.** Fecha o
     item 10 da rodada 2. Deriva da localização que o produto já exige
     (decisão 7), sem coletar nada novo.

     Geocodificação reversa por provedor externo (Google/Mapbox/etc.)
     mandaria a posição exata para fora da API a cada checagem —
     contradiz diretamente a decisão 135 ("posição exata nunca sai da
     API") e criaria uma dependência de provedor comercial para uma
     verificação que não precisa de rede. Decisão: **dataset estático de
     fronteiras de país embarcado na API** (ex. Natural Earth, licença
     livre), checado em memória por point-in-polygon — zero chamada
     externa, zero custo por request, zero vazamento de posição. Caso raro
     em que a decisão 143 (port por provedor) nem se aplica: não há
     provedor a encapsular, é dado estático + função pura.

     **Fronteira ativa não invalida caso em andamento**: uma denúncia já
     criada continua valendo mesmo que o denunciante ou helper cruze a
     fronteira depois — o vínculo se formou sob a jurisdição de origem.
     Só a **criação de nova ação** (nova denúncia, nova oferta de ajuda)
     checa o país atual a cada vez.

     **Rodada 2 do Legal Gate FECHADA por completo** (decisões 103–109,
     143–146) — restam só escolhas comerciais (provedor da L2, decisão
     144), nunca arquitetura.

## Fora de escopo para esta fase

- Previsão de trajetória por modelo de velocidade + notificação push
  proativa (decisão 11) — visão documentada, implementar em fase futura.
- Categoria "policial validado" e seu fluxo de validação (decisão 12) —
  fase futura.
- Regras legais de recompensa/LGPD-equivalentes fora do Brasil (decisão 8)
  — modelo de dados preparado; o *conteúdo* das regras por país continua
  não implementado, mas o **mecanismo** que as enforça passa a existir
  (decisão 76). Até haver regra declarada, cada país fica bloqueado por
  `no_control`, que é o comportamento pretendido.
- **Proteção contra apropriação da ideia** — o Legal Gate trata de execução,
  não de propriedade, e não resolve isto. O ativo que serve para isso já
  existe: este documento (decisões numeradas, datadas, nunca renumeradas,
  com o raciocínio preservado) é registro de anterioridade. O que falta é
  torná-lo **verificável por terceiro** — histórico de repositório assinado
  ou hash do documento publicado periodicamente. Barato, fora do escopo
  desta frente, e deveria virar decisão própria.
- **Moderação de conteúdo das denúncias** (Marco Civil art. 19 — remoção por
  ordem judicial) — frente separada; o gate bloqueia capacidade, não
  conteúdo.

## Reward — recebedores fixados na reserva (achado ao abrir o domínio)

147. **Os recebedores da recompensa são fixados no momento em que a reserva
     é criada (`reserve`), não descobertos depois pela mediação.** Emenda
     a decisão 100 item 2 (decisões 36/37 — spec vinculante, emenda antes
     de divergir): ao tentar abrir o domínio Reward em cima do
     `PaymentRail`, ficou claro que "pagar os helpers, no plural, decididos
     pela mediação" era incompatível com dois fatos já fechados — a
     decisão 95 tira o dinheiro da conta do denunciante **no momento da
     oferta** (Pix, sem pré-autorização), e o Asaas (candidato de PSP,
     decisão 144-style) fixa o split **na criação da cobrança**, não na
     liberação. Não dá pra reter dinheiro para um recebedor que ainda não
     existe.

     **Consequência de fluxo**: a recompensa nasce **sem reserva**
     (decisão 88, opção 1) desde a criação da denúncia — pode ficar assim
     indefinidamente, decisão 30 continua obrigando o denunciante do mesmo
     jeito. **Reservar via Pix é uma ação posterior**, disponível só
     quando o denunciante já sabe a quem quer garantir o pagamento — ou
     seja, contra help offers que já existem no momento da reserva. A
     reserva referencia um conjunto fixo de `(helpOfferId, amountCents)`;
     esse conjunto não muda depois.

     **O que isso simplifica na mediação (decisão 98)**: mediar deixa de
     ser "escolher quem recebe" e passa a ser **julgar se a condição foi
     cumprida** para o conjunto já fixado — resultado binário por reserva:
     `capture` (libera exatamente para quem foi fixado) ou `cancel`
     (devolve ao denunciante). Decisão 30(c) (N helpers simultâneos)
     continua valendo — o conjunto fixado pode ter mais de um — só deixa
     de ser "descoberto depois".

     **Não resolvido aqui, registrado como aberto**: reforçar/ampliar uma
     reserva já criada (ex. mais um helper apareceu depois de reservado)
     não tem mecanismo — hoje exigiria cancelar e criar reserva nova.
     Fica para quando houver caso real que precise disso; não é MVP.

     Destrava a abertura do domínio Reward (`api/docs/feature/reward.md`).

148. **Toda resolução de mediação exige duas pessoas distintas — sem
     limiar de valor.** Fecha o "candidato natural acima de um valor" da
     decisão 98: o limiar não existe, o duplo controle é incondicional.
     Toda resolução instrui movimento de dinheiro de terceiro; a fricção
     de um segundo aprovador é pequena perto do risco, e a ausência de
     limiar elimina uma configuração a manter e um vetor de erro (limiar
     mal calibrado). Mecânica no padrão do descongelamento (141d):
     mediador A **propõe** o desfecho (fulfilled/not_fulfilled, com
     justificativa), mediador B — obrigatoriamente outra pessoa —
     **aprova**. Se o volume um dia tornar isso caro, cria-se limiar por
     decisão nova; começar permissivo e apertar depois é o sentido errado.

149. **A contestação acontece ANTES da execução: janela entre a aprovação
     e o capture/cancel.** Fecha a "via de contestação" da decisão 98.
     Pix liberado não volta (decisão 92) e devolução consumada tampouco —
     contestação pós-fato seria um formulário sem remédio. Logo: a
     resolução aprovada **não executa na hora**; abre-se uma janela (dias
     em config, `MEDIATION_CONTEST_WINDOW_DAYS`, default 7 — cabe dentro
     do prazo de retenção do PSP) em que as **partes do caso** (o
     denunciante pagador e os helpers do conjunto fixado pela 147) podem
     registrar contestação. A execução no PSP é uma ação humana posterior
     no painel — sem job agendado — permitida só com a janela vencida e
     nenhuma contestação aberta. Contestação aberta trava a execução até
     um mediador fechá-la com nota (registrada no log imutável) ou a
     resolução ser cancelada e proposta de novo (novo ciclo da 148).
     Enquanto não executada, a reserva segue viva no PSP — o selo da
     decisão 85 continua verdadeiro durante a janela.

150. **A versão dos critérios de mediação que governa um caso é a que
     estava ativa quando a reserva foi criada — carimbada na oferta.**
     Fecha o "critérios publicados antes do caso" da decisão 98 no mesmo
     padrão do `no_return_notice_version` (decisões 86/92): publicar
     critérios é criar **versão imutável** (append-only; corrigir =
     publicar versão nova), a versão ativa no momento do `reserve` fica
     gravada na oferta, e a mediação julga por ela — publicar versão nova
     não muda a regra de casos já reservados. Consequência dura: **sem
     critérios publicados, não há reserva** — o `reserve` falha com erro
     tipado, porque garantia sob regra não declarada é exatamente o que a
     98 chama de fachada. Os critérios são visíveis no app (regra do jogo
     das partes), e o texto em si passa pelo advogado junto com os demais
     textos jurídicos (pendência das decisões 25/30/45/57 — via Legal
     Gate, não bloqueia o mecanismo).

## Auth de usuários do app (rodada 9 — fecha os itens 2–3 da rodada 6)

Decidido em 2026-08-22 via `AskUserQuestion` (Valdo escolheu a opção
recomendada). Contexto: `plano-auth-usuarios.md` §"Pendências (rodada
6)"; a API (`/app-auth`) tem senha/sessão/vínculo prontos desde
2026-08-03 (decisão 119), mas o app não tinha nenhuma tela de login/
cadastro até este momento.

151. **Verificação de e-mail do app reaproveita o mailer do painel**
     (`shared/mailer`, decisão 113), com TTL e contador PRÓPRIOS do app
     — não o mesmo registro do painel. Fecha o item 2 da rodada 6.
     Continua valendo a decisão 123: a verificação nunca bloqueia
     denunciar, só ações consequentes (oferecer/reivindicar recompensa,
     virar respondedor).

152. **Adapters de provedor social (Google/Apple/Facebook) ficam
     adiados até existir credencial OAuth real** (client id/secret nos
     três consoles) — sem o SDK cliente configurado não há como
     descobrir o formato real do token para verificar (mesma razão já
     registrada na rodada 6, item 3). Fecha o item 3 SEM construir os
     adapters agora: o app ganha cadastro/login por e-mail+senha
     (método que já está pronto na API), social entra depois como
     adição — `loginWithProvider` já aceita identidade pré-verificada,
     então plugar um adapter não muda nenhuma regra existente. OTP
     (item 1 da rodada 6) continua bloqueado na escolha comercial do
     provedor de envio, mesma natureza da decisão 59.

## Validadores compartilhados do app (rodada 10 — fecha o gap 4 da auditoria TDD)

Decidido em 2026-09-02 (Valdo respondeu "1C, 2ii, 3ii, 4iii, 5i" às
pendências de `plano-validadores.md` §7). Contexto: a auditoria TDD de
2026-08-22 apontou `packages/vgr_validators` como boilerplate morto (só o
`Calculator` do template, zero consumidores); ao levantar evidência, a
hipótese de "validação duplicada espalhada" NÃO se confirmou — o app
quase não valida formato no cliente (confia no 422 por `code`, decisão
83), e o espelho `api/src/shared/validation` prometido no pubspec do
pacote nunca existiu.

153. **`vgr_validators` é construído no mínimo, sob demanda** — fecha o
     item 1 (opção C). O `Calculator` sai; entram só as regras de formato
     que um formulário existente já exige: CPF/CNPJ, telefone BR, CEP e
     e-mail (hoje: onboarding do helper, decisão 143) + máscara de
     digitação. Não se cria módulo de validação compartilhado na API
     agora (isso seria a opção B, que fica como evolução natural quando
     surgir o segundo formulário com campo de formato). Descontinuar (A)
     foi recusado: o cliente DEVE dar feedback imediato de formato,
     especialmente com a fila offline (28), onde o 422 chegaria horas
     depois. Invariante que continua: a API sempre revalida (47, 110) —
     validação de cliente é conforto, nunca segurança.

154. **A verdade da regra de formato é o Zod inline do DTO da API; o
     teste do app cita o DTO espelhado** — fecha o item 2 (opção ii).
     Enquanto não existir `api/src/shared/validation`, cada validador do
     app leva comentário `// mirrors <arquivo>.dto.ts <schema>` e um teste
     por borda (mínimo, máximo, dígito verificador) que prova que a regra
     do app é IDÊNTICA à do DTO. Divergência descoberta → invariante 5
     (emenda antes de divergir), nos dois lados no mesmo commit.

155. **CPF/CNPJ com dígito verificador NOS DOIS LADOS** — fecha o item 3
     (opção ii). A API endurece `taxId`/`payerTaxId` em `reward.dto.ts`
     (hoje só tamanho 11–14) para validar os dígitos verificadores; o app
     aplica a mesma regra. Motivo: regra idêntica (154) e não mandar
     documento inválido ao PSP (Asaas) — rejeição do PSP custa round-trip
     e mensagem opaca. Máscara/normalização: o app envia só dígitos
     (`unmask`), a API aceita só dígitos.

156. **Guard contra validação inline em tela NÃO entra agora** — fecha o
     item 4 (opção iii). As três telas do admin com `length < N` inline
     (`case_freeze_page`, `legal_rules_page`, `legal_capabilities_page`)
     ficam como estão. Registrado em "Fora de escopo" para reabrir junto
     com a opção B (153), quando o guard passa a fazer sentido por haver
     mais de um consumidor. Enquanto isso, a regra é disciplina de
     review (110): tela nova com campo de formato usa `vgr_validators`,
     não `RegExp(` inline.

157. **`TextInputFormatter` de máscara vive em `vgr_validators`;
     `VgrTextField` ganha `mask: VgrMask?` e consome o formatter** —
     fecha o item 5 (opção i). Divisão: validators = funções puras +
     formatter (dependência só de `flutter/services`), sem widget e sem
     tradução; widgets = sem regra de formato, só recebem o enum e montam
     `inputFormatters`; tela = passa o enum, nunca toca `TextInputFormatter`
     direto (133). Mensagem de erro continua da tela via `code` (83) — o
     validador devolve um `code`, não texto.

## Busca, moderação e estatísticas do painel (rodada 11 — abre a frente 142)

Decidido em 2026-09-02 (Valdo respondeu "1 recomendado, 2i, 3i, 4i, 5i,
6i, 7 recomendado, 8 aceito, 9i, 10i" às pendências de
`plano-moderacao-painel.md` §8). Contexto: a frente da denúncia está
completa, mas o painel só congela caso por id; não há busca, não há
como tirar denúncia/mídia do ar (o status `blocked` da mídia existe e
nenhum endpoint o escreve), não há agregação.

158. **A frente entrega cinco fases, na ordem B1 → B2 → B4 → B3 → B5** —
     fecha o item 1. B1 busca + detalhe do caso no plano do painel; B2
     moderação; B4 estatísticas; B3 fila; B5 tela da trilha
     `tb_admin_audit`. Estatísticas antes da fila porque a fila depende
     de sinal que só existe a partir da 161; a trilha entra porque a 166
     passa a auditar leituras — auditar sem ter como ler é metade da 116.
     Cada fase com liberação própria (38), suíte verde, feature doc e
     commit.

159. **No painel a posição do caso é DEGRADADA por padrão; a exata sai só
     com grant próprio, sem bootstrap, e cada leitura é auditada** — fecha
     o item 2 (opção i). O detalhe serve a posição pela mesma grade do
     feed (`shared/geo/degrade`, 135). A interface kind 'R'
     `report_exact_position` (VIEW) não recebe bootstrap — como o
     `media_original` (130): ninguém a tem até um humano conceder — e a
     leitura exata grava `tb_admin_audit` (action `read`, entity
     `report_position`). É o "fluxo auditado" que a 135 previa.

160. **Denúncia NÃO anônima mostra ao painel só o id opaco da conta e o
     displayName; nunca e-mail** — fecha o item 3 (opção i). O operador
     precisa reconhecer reincidência, e o id basta para isso. Denúncia
     anônima continua sem nenhuma identidade no painel: o
     `reporter_account_id` interno e o accountability log seguem fora de
     qualquer resposta (23/44/45/60); o reveal é o fluxo da 45, não desta
     frente.

161. **Fila de moderação proativa: casos abertos ainda não revisados,
     priorizando tier alto e presença de mídia; revisar é marcar
     `reviewed_at`/`reviewed_by`** — fecha o item 4 (opção i). Não existe
     "sinalizar conteúdo" pelo usuário; construir isso é frente mobile
     própria (capacidade nova, Legal Gate), registrada em "Fora de
     escopo" e reaberta quando o produto tiver usuários para sinalizar.
     Quando existir, o sinal entra na MESMA fila como prioridade acima do
     tier.

162. **Moderação = bloquear mídia, ocultar denúncia e reverter os dois;
     cada ato é de UM humano, com motivo obrigatório e auditoria;
     modelagem por coluna própria, não por `status`** — fecha o item 5
     (opção i). Reverter não destrói nada, logo não pede dual-control —
     esse padrão fica reservado ao que reabilita destruição (141d/107).
     `tb_report` ganha `hidden CHAR(1)`, `hidden_reason_code`,
     `hidden_note`, `hidden_at`, `hidden_by`; `tb_media.status` passa a
     ser escrito (`available ↔ blocked`) por endpoint do painel, com as
     mesmas colunas de motivo. Ocultar/bloquear NÃO altera retenção,
     expiração nem purge (25/131): moderação não é apagamento. Caso
     oculto some do feed, da busca pública e do detalhe de terceiros;
     dono e participantes continuam vendo (com a marca da 167). Mídia
     bloqueada some do plano do app e continua legível no painel (M3).

163. **Motivo de moderação: catálogo fixo em código + nota livre
     obrigatória quando `other`** — fecha o item 6 (opção i). Códigos
     canônicos em inglês (17): `spam`, `abuse`, `illegal_content`,
     `duplicate`, `personal_data`, `other`. É o código que as
     estatísticas contam; catálogo administrável é evolução (mesma
     trajetória do risk-config, 140d).

164. **Estatísticas: contadores agregados por período × categoria ×
     sujeito × status × tier, mais congelados/ocultos/expirados/purgados
     e motivos de moderação; piso de agregação k = 5; sem mapa de calor
     nesta rodada** — fecha o item 7. Qualquer célula com contagem menor
     que 5 é servida como "<5", para que combinação rara não
     reidentifique (mesma lógica da 41 aplicada a agregados). Mapa de
     calor (só na grade `high`) reabre quando houver volume real.

165. **Interfaces e privilégios da frente** — fecha o item 8: `reports`
     (kind 'T', grupo "Operations"; VIEW = buscar/ver, UPDATE = moderar e
     marcar revisado), `report_exact_position` (kind 'R', VIEW, sem
     bootstrap — 159), `report_stats` (kind 'T', VIEW), `admin_audit`
     (kind 'T', VIEW — B5). `case_freeze` e `media_evidence` ficam
     intactos: o detalhe do caso embute o bloco de congelamento chamando
     `/api/case-freeze` e habilita seus botões pelo grant de
     `case_freeze`; a imagem continua servida por `/api/media` sob
     `media_evidence`. Bootstrap de `reports`/`report_stats`/`admin_audit`:
     de-facto admins (UPDATE em Users), padrão de 020/021/022.

166. **Ler o detalhe de um caso no painel grava auditoria; ler a lista
     não** — fecha o item 9 (opção i). Texto livre, campos de detalhe e
     timeline são evidência da mesma natureza que a foto (130). Uma linha
     por abertura de detalhe (action `read`, entity `report`); a lista
     paginada não gera linha (auditar listagem afogaria a trilha, 116).
     A tela da trilha (B5) entra nesta frente como última fase.

167. **O dono vê a marca `hidden` no próprio detalhe, sem motivo e sem
     evento de timeline** — fecha o item 10 (opção i). O caso some do
     feed e o dono merece um estado explícito; o motivo é da auditoria,
     não do denunciante (evita dar ao abusador o roteiro do que passou).
     Participantes veem a mesma marca. Timeline continua append-only
     sem esse evento — mesma escolha do congelamento (141), por razão
     diferente.

     **Rodada 11 ZERADA** (decisões 158–167).

## Chat mascarado denunciante ↔ helper (rodada 12 — abre a decisão 54)

Decidido em 2026-09-03 (Valdo respondeu "1 sim | 2i | 3i | 4i | 5ia | 6
aceitar | 7i | 8i | 9 sim | 10 aceitar" às pendências de `plano-chat.md`
§8). Contexto: a 54 colocou o chat no MVP e a spec tática desenhou
`ChatThread`/`MaskedIdentity`, mas o laço denunciante ↔ helper termina
hoje na oferta de ajuda; não há infra de push, SSE nem websocket; o
helper que ofereceu ajuda SEM conta não tem identidade roteável no
servidor (`helper_account_id` NULL).

168. **Três fases, C1 API → C2 mobile → C3 painel, cada uma liberada por
     "pode seguir"** — fecha o item 1. C3 é pequena e encaixa no detalhe
     do caso da frente 142.

169. **Só conversa quem tem identidade roteável: helper com conta (mesmo
     tendo escolhido anonimato — a máscara cobre) e denunciante com conta
     OU com `x-client-key`. Helper sem conta não tem chat e é avisado
     ANTES de oferecer** — fecha o item 2 (opção i). Mesmo padrão do aviso
     "sem conta não reivindica recompensa" (34). "A denúncia nunca espera"
     (123) protege o denunciante; não obriga a plataforma a manter canal
     com quem não pode ser encontrado. Quem quer conversar cria conta e
     continua anônimo pela máscara. Nenhum segundo segredo portador.

170. **Cada lado vê do outro exatamente o que a oferta já mostrava** —
     fecha o item 3 (opção i). Rótulos fixos "Denunciante" / "Ajudante";
     nome de exibição do helper só quando ele escolheu identificar-se E o
     tier não é high (6/40/60); o denunciante nunca mostra nome no chat;
     outros helpers nunca veem a thread (55). No payload, cada
     participante é um token opaco por (thread, participante), nunca
     reusado entre reports (spec `MaskedIdentity`). Nenhuma superfície
     pode ser mais permissiva que a oferta.

171. **Contato direto é BLOQUEADO no servidor, com espelho no app** —
     fecha o item 4 (opção i). Telefone (≥ 8 dígitos com ou sem
     máscara), e-mail, URL, `@handle` e apps de mensagem seguidos de
     número são recusados com 422 e `code` próprio (`CONTACT_NOT_ALLOWED`),
     apontando o trecho. A regra vive em `shared/` na API e é espelhada
     em `vgr_validators` (154) para feedback antes do envio. 54 diz "sem
     compartilhar", não "com aviso". Texto máximo 1000 caracteres.

172. **Entrega por polling com cursor; mensagem entra na fila offline com
     `clientKey`** — fecha o item 5 (opções i + a). `GET …/messages?after=<id>`
     com intervalo curto só com a tela aberta, sem background; contagem
     de não lidas ao abrir o detalhe do caso. Idempotência por chave
     gerada no app, como a denúncia (137): replay devolve a mesma mensagem.
     Push proativo continua visão (11); SSE/websocket ficam para quando
     houver volume que justifique infra nova.

173. **Ciclo de vida do chat segue o do caso** — fecha o item 6. Thread
     nasce find-or-create na PRIMEIRA mensagem do helper com oferta (spec).
     Caso resolvido: escrita fechada, leitura mantida até o purge (18/131).
     Caso oculto (162): escrita fechada, leitura mantida. Caso congelado
     (141): tudo segue, nada expira. Purge (131): texto das mensagens
     zerado, esqueleto (contagens, timestamps) mantido para estatística —
     mesma régua do `purgeReport`.

174. **Timestamp de mensagem é degradado por tier para o outro lado; não
     há recibo de leitura** — fecha o item 7 (opção i). `TIME_MS_BY_TIER`
     (minuto / 15 min / hora, 41/135); ordem preservada pelo id. "Visto"
     é sinal temporal a mais e fica fora do MVP.

175. **Painel lê o chat de um caso sob grant próprio `chat_evidence` (kind
     'R', VIEW, SEM bootstrap), cada leitura auditada; sem escrita; sem
     ocultar mensagem individual nesta frente** — fecha o item 8 (opção
     i). Mesmo padrão do `media_original` (130) e da posição exata (159):
     ninguém tem o grant até um humano conceder. Ocultar o caso inteiro
     (162) já fecha o canal; moderação por mensagem reabre com "sinalizar
     conteúdo" (161).

176. **`chat.masked` é capacidade do Legal Gate, nasce em `PENDING_WIRING`
     e é cabeada na C1** — fecha o item 9. Chat entre anônimos tem risco
     jurídico que varia por país tanto quanto mídia (138); bloqueado →
     451 antes de qualquer escrita.

177. **Limites fixos do MVP: 30 mensagens/min por thread, 1000 caracteres,
     texto simples sem mídia, append-only (sem editar/apagar pelo
     autor)** — fecha o item 10. Os números viram configuração de
     ambiente (`CHAT_RATE_PER_MINUTE`, `CHAT_MAX_LENGTH`), não decisão.

     **Rodada 12 ZERADA** (decisões 168–177).

## Rating de helpers pelo denunciante (rodada 13 — abre a decisão 48)

Decidido em 2026-09-03 (Valdo respondeu "1 sim | 2 i-a | 3 i | 4 i | 5 i |
6 i | 7 i | 8 i | 9 i | 10 i-b | 11 i | 12 i" às pendências de
`plano-rating.md` §8). Contexto: a 48 criou o rating do helper pelo
denunciante "ao finalizar a denúncia", acumulando na identidade interna;
a spec tática desenhou `HelperRating`/`RatingScore`/`RateHelper`. A
rodada 0 achou que a API resolve a denúncia
(`POST /app-reports/:id/resolve`) mas nenhuma tela do mobile chama esse
endpoint; que `tb_help_offer` não tem status nem aceite; que helper com
conta anônimo tem `helper_account_id` gravado (23/32) e helper sem conta
não tem identidade interna nenhuma — o mesmo problema que a 169 fechou no
chat.

178. **Três fases, RT1 API → RT2 mobile → RT3 painel, cada uma liberada
     por "pode seguir"** — fecha o item 1. RT3 é pequena e encaixa no
     detalhe do caso da frente 142, no mesmo padrão da 168.

179. **O encerramento da denúncia pelo app entra nesta frente (RT2), sem
     campo de desfecho** — fecha o item 2 (opção i-a). Sem encerrar não
     há "finalização" (48). Botão só para o dono (conta ou
     `x-client-key`, 134), com confirmação, enviado pela fila offline
     (28/137); a retenção de 90 dias já corre da resolução (131).
     Desfecho (resolvido com ajuda / sem ajuda / desisti) em `tb_report`
     fica registrado como visão — é decisão de produto à parte.

180. **Só helper com conta é avaliável, mesmo tendo escolhido anonimato
     — a máscara cobre; helper sem conta não recebe avaliação e é avisado
     ANTES de oferecer** — fecha o item 3 (opção i). Mesma régua da 169:
     a conta é gravada sempre que existe (23/32), então a reputação
     acumula na identidade interna sem expor nada a ninguém (48/60).
     Nenhum segundo segredo portador. O aviso da 169 passa a dizer "sem
     conta não há chat nem reputação".

181. **Avaliação só com o caso resolvido: no fluxo de encerramento e,
     depois, no detalhe do caso, até o purge (131); avaliar nunca é
     obrigatório para encerrar** — fecha o item 4 (opção i). "A denúncia
     nunca espera" (123) vale para o fechamento também. Avaliar com o
     caso aberto seria sinal de engajamento em tempo real (41) e
     instrumento de pressão sobre o helper.

182. **Nota inteira de 1 a 5, sem texto** — fecha o item 5 (opção i).
     Spec `RatingScore`. Texto livre é canal de retaliação e de contato
     (54/171) e exigiria filtro e leitura no painel; comentário curto
     visível só ao painel fica como visão, se a moderação precisar de
     evidência.

183. **Uma avaliação por oferta, imutável** — fecha o item 6 (opção i).
     Append-only como o chat (177): segunda tentativa → 409
     `ALREADY_RATED`; replay do mesmo `clientKey` devolve a mesma
     avaliação (137).

184. **Helper vê só o próprio agregado (contagem e média), e a média só a
     partir de 5 avaliações; nunca a nota por caso** — fecha o item 7
     (opção i). Piso k=5 das 164/165: com poucas avaliações o agregado
     revela a individual, e "o caso X me deu 1" aponta o denunciante e
     alimenta retaliação (6/40).

185. **Nenhum usuário vê reputação de outro no MVP** — fecha o item 8
     (opção i). Spec 003: `RatingScore` "nunca num perfil público".
     Reputação serve ao próprio helper (184) e, no futuro, ao peso da 27
     (189). Faixa qualitativa ou média na oferta ficam como visão, para
     quando houver volume — e nunca em tier high (41).

186. **Painel vê a nota por oferta no detalhe do caso, sob a interface
     `reports` já existente; sem tela de agregado por helper** — fecha o
     item 9 (opção i). É conteúdo do caso, não identidade (o painel já
     vê o `accountId` opaco do helper, 160). Distribuição de notas nas
     estatísticas (164) fica como visão.

187. **Rating sobrevive ao purge do caso; avaliação de caso oculto fica
     fora do agregado enquanto o caso estiver oculto** — fecha o item 10
     (opção i-b). Reputação não é evidência: a linha guarda ids e nota,
     nada a zerar (mesma lógica do esqueleto do chat, 173). Caso oculto
     (162) é suspeita de abuso, e o par denunciante/helper fraudulento é
     o vetor óbvio de inflar reputação — sai do agregado na leitura e
     volta ao reexibir. Congelamento (141) não muda nada.

188. **`helper.rating` é capacidade do Legal Gate, nasce em
     `PENDING_WIRING` e é cabeada na RT1** — fecha o item 11 (opção i).
     Reputação é perfilamento de pessoa; o risco varia por jurisdição
     tanto quanto o chat (176); bloqueado → 451 antes de qualquer escrita.

189. **O peso de confiança da 27 fica fora desta frente; a RT1 só deixa
     o agregado por identidade interna legível** — fecha o item 12
     (opção i). A fórmula nasce na rodada de direction sightings, quando
     houver consumidor — regra sem consumidor é regra sem teste.

     **Rodada 13 ZERADA** (decisões 178–189).

## Botão de pânico (rodada 14 — fecha a pendência 52, abre 62–65)

Decidido em 2026-09-04 (Valdo respondeu "1 i | 2 i | 3 i | 4 i | 5 i | 6
i | 7 i | 8 i | 9 i | 10 i" às pendências de `plano-panico.md` §8).
Contexto: a 51 desenhou o pânico com um pool restrito de "respondedores
autorizados" e deixou o critério de autorização pendente (52); as
decisões 62–65 corrigiram o pânico pra fora do fluxo de denúncia, com
dois níveis de acessibilidade e destinatário configurável em dois
modos. A rodada 0 achou que o pool de respondedores já tem código
(`api/src/modules/panic/responder-pool.*`, migração 012, tela admin em
`apps/admin/.../panic-responders/`), mas o `PanicAlert` propriamente
dito não tem nenhuma linha; achou também que o `POST` de pedido de
autorização está montado no plano administrativo da API, inalcançável
por um usuário do app — correção de posicionamento de plano (119),
aplicada na construção, não decisão de negócio.

190. **Critério de respondedor autorizado: julgamento humano livre, sem
     regra codificada** — fecha a pendência 52. O pré-requisito já
     construído (`criteria_notes` texto livre, decisão do administrador
     caso a caso) é o desenho final, não um rascunho a substituir; a
     tela de aprovação já existente continua funcionando sem mudança.

191. **Um alerta é um tiro único: posição no acionamento, sem sessão
     viva** — fecha o item 2. MVP menor, sem gateway de geolocalização em
     stream; a "geolocalização contínua" do texto das decisões 62–65 fica
     satisfeita pela posição capturada no momento do clique, sem
     atualização automática enquanto o alerta segue ativo. Revisita a
     linguagem original das 62–65 nesse ponto específico.

192. **Entrega ao respondedor por uma tela própria de alertas, com
     polling por cursor** — fecha o item 3. Mesmo padrão do chat
     (decisão 172): `after=<id>`, intervalo curto só com a tela aberta,
     sem background. Push proativo continua fora do MVP (11), mesma
     aceitação já registrada no evento `PanicAlertTriggered` da spec.

193. **Contato de confiança (64, segundo modo) fica fora desta rodada** —
     fecha o item 4. Só o modo pool de respondedores sai agora; contato
     pessoal — com ou sem conta VGR, com ou sem SMS — fica registrado
     como visão futura, evitando depender do provedor comercial ainda
     pendente (mesma família da decisão do OTP).

194. **Modo ativado/em destaque (63) fica fora desta rodada** — fecha o
     item 5, amarrado à 193: sem contato de confiança pra pré-configurar,
     o valor do modo opt-in fica pequeno demais pra justificar construí-lo
     agora. Só o botão padrão (uso a frio, decisão 65) sai nesta frente.

195. **Distância mostrada ao respondedor reaproveita
     `DISTANCE_STEP_BY_TIER`** — fecha o item 6. A régua já existe em
     `shared/geo/degrade.ts`, distinta da degradação de posição bruta dos
     reports, e já parece feita sob medida para exatamente isto.

196. **Mensagem do alerta é um modelo fixo, sem texto livre do usuário** —
     fecha o item 7. Consistente com a decisão 65 ("sem exigir mais
     informação do usuário no momento do clique"); evita abrir uma
     superfície nova de moderação/filtro de contato (171) só para o
     pânico.

197. **Só quem acionou o alerta pode resolvê-lo** — fecha o item 8. Um
     respondedor não encerra um alerta que não é dele; "estou seguro
     agora" é ato exclusivo de quem está em risco. Sem resolução por
     tempo — o alerta não expira sozinho.

198. **Anti-abuso: cooldown simples — não é possível abrir um novo alerta
     enquanto o anterior do mesmo usuário segue ativo** — fecha o item 9.
     Sem sistema de detecção de fraude nem limite por período nesta
     frente; o cooldown evita só o clique duplicado/spam básico, sem
     risco de bloquear uma emergência real subsequente (o alerta anterior
     precisa estar resolvido primeiro, ato do próprio usuário, 197).

199. **Fatiamento: PP1 API → PP2 mobile padrão → PP3 mobile avançado (se
     houver) → PP4 painel (se houver)**, cada fase por "pode seguir" (38),
     API sempre sem pendência antes da próxima fase — fecha o item 10.
     PP3 e PP4 ficam condicionais: as 193/194 já tiram boa parte do
     escopo avançado; PP4 provavelmente não terá conteúdo (a tela de
     aprovação já existe e não muda).

     **Rodada 14 ZERADA** (decisões 190–199).

## Apontamentos de direção / Direction Sighting (rodada 15 — decisões 22, 26, 27)

Decidido em 2026-09-04 (Valdo respondeu "1 i | 2 i | 3 i | 4 i | 5 i | 6
i | 7 i | 8 i" às pendências de `plano-direction-sightings.md` §8).
Contexto: as decisões 22/26/27 já fixaram processamento síncrono,
reconciliação estatística ponderada com prior 50/50 e peso menor pro
apontamento anônimo, mas nenhum código nunca existiu além da spec
tática. A rodada 0 achou que a rota que a spec desenhava
(`POST /api/direction-sightings`) tem o mesmo bug de plano já corrigido
no pânico, e que a capacidade `location.tracking` do Legal Gate já
existe, `PENDING_WIRING`, citando literalmente as decisões 7/22/26.

200. **Qualquer pessoa que veja a denúncia aberta pode apontar uma
     direção, anônima ou identificada — só o próprio denunciante fica de
     fora** — fecha o item 1. Mesmo alcance de "coletivo pela comunidade"
     do texto original, e mesmo raciocínio anti-fraude da decisão 20:
     quem denunciou não deveria poder manipular a estimativa do próprio
     caso.

201. **Elegibilidade por categoria é fixa no código, mesmo padrão já
     usado no raio dinâmico (`dynamic-radius.ts`)** — fecha o item 2.
     Mais simples, sem tela de admin nova; a lista pode ser promovida a
     configurável no futuro se precisar mudar com frequência, mas não há
     evidência disso agora.

202. **Piso mínimo de 5 apontamentos antes de expor qualquer direção,
     configurável por variável de ambiente** — fecha o item 3. Formaliza
     o "cuidado de design" original (agregar antes de expor, para não
     alertar quem está sendo rastreado); o número é o mesmo já usado no
     piso de k-anonimato das estatísticas do painel (164/165) por
     consistência, embora o motivo aqui seja outro (contravigilância,
     não anonimato estatístico).

203. **Só a direção mais provável é exposta, nunca a distribuição de
     probabilidade completa** — fecha o item 4. Menor informação
     possível, mesmo princípio já aplicado em toda a degradação de
     posição, distância e mascaramento do projeto.

204. **A direção é exposta a todo mundo que vê a denúncia aberta,
     incluindo o feed público, uma vez passado o piso da 202** — fecha o
     item 5. Mantém o alcance de "mais gente ajuda a rastrear" do texto
     original.

205. **Peso do apontamento (identificado vs. anônimo, decisão 27) é
     valor fixo no código com ajuste por variável de ambiente** — fecha
     o item 6. Mesmo tratamento que os limites do chat (177) já
     receberam: número operacional, não decisão travada.

206. **O peso de confiança da reputação (rating, RT1–RT3) NÃO entra
     nesta rodada** — fecha o item 7 e a promessa da decisão 189. A
     fórmula do apontamento fica só identificado vs. anônimo (27, 205);
     incorporar a média de avaliações do helper fica registrado como
     refinamento futuro, quando houver evidência de que o peso simples
     não basta — mesmo raciocínio que a 189 já usava: regra sem
     consumidor validado é regra sem teste.

207. **Fatiamento: DS1 API → DS2 mobile → DS3 painel (DS3 fica vazia,
     dado que a 201 escolheu o padrão fixo no código, sem tela de
     admin)**, cada fase por "pode seguir" (38), API sempre sem
     pendência antes da próxima fase — fecha o item 8.

     **Rodada 15 ZERADA** (decisões 200–207).

## Oferta de ajuda com vários tipos (rodada 16 — revisa a leitura singular da decisão 10)

Aberta e fechada em 2026-09-11, a partir do pedido de Valdo no primeiro
teste com dois atores reais (2026-09-10): a tela de oferta usava
checkboxes mas só aceitava um tipo. Plano executivo:
[plano-oferta-multitipo.md](../plans/plano-oferta-multitipo.md).

208. **Uma oferta por helper por denúncia, com um CONJUNTO de tipos de
     ajuda (mínimo um, sem repetição).** A decisão 10 lista as frentes;
     o helper pode atuar em várias ao mesmo tempo e o app não tem como
     limitar isso. A oferta continua sendo o vínculo helper ↔ denúncia
     (`uq_offer_helper` fica); chat (168–177), rating (178–189) e
     recompensa (147) seguem pendurados na oferta, não no tipo. A
     alternativa "várias ofertas, uma por tipo" foi descartada por
     multiplicar rating/chat. Emenda a spec 003 (`submitHelpOffer`
     recebe `HelpType[]`, evento `HelpOfferSubmitted { helpTypes }`) e
     os cenários 004.

209. **Persistência em tabela filha `tb_help_offer_type (tb_help_offer_id,
     help_type)`**, chave primária composta, CHECK na lista da 10, FK com
     cascata. Sem JSON (reservado ao `detail_fields`, validado por
     schema) e sem bitmask.

210. **A coluna `tb_help_offer.help_type` é REMOVIDA após o backfill**
     (uma linha na filha por oferta existente). Uma única fonte de
     verdade; "tipo principal" não existe.

211. **O helper pode ALTERAR os tipos da sua oferta enquanto a denúncia
     estiver aberta** — o usuário pode ter marcado errado. `PUT
     /app-help-offers/:id/types { helpTypes }`, mesma validação do
     envio, só pelo helper dono da oferta e só em denúncia aberta (18);
     substitui o conjunto inteiro. Restrição estrutural: oferta ANÔNIMA
     não tem identidade nem client key (032) — não há como provar que é
     do mesmo aparelho —, logo só a oferta identificada é editável; a
     anônima fica como está (mesma lógica da 169 para o chat).

212. **Linha do tempo: um único item `help_offered` com `helpTypes: []`**;
     a edição da 211 gera um item `help_offer_updated { helpTypes }`.
     Um item por tipo não representa evento real.

213. **Contrato da API só com `helpTypes: []`** (1..5 valores da lista,
     sem repetição; 422 `VALIDATION` fora disso). `helpType` singular
     deixa de existir — não há cliente fora deste repositório. Visões
     dono/participante e detalhe do painel devolvem `helpTypes` por
     oferta.

214. **Fatiamento: HT1 API → HT2 mobile → HT3 painel**, cada fase por
     "pode seguir" (38), API sem pendência antes da próxima (método
     2026-09-04). Fora de escopo, registrado: oferta anônima na própria
     denúncia é aceita (o veto da 20 só enxerga conta) — limitação
     conhecida, coerente com a 23.

     **Rodada 16 ZERADA** (decisões 208–214).

## Painel admin no modelo do setes-app (rodada 17 — aplica a decisão 15 ao shell do painel)

Aberta e fechada em 2026-09-21. Pedido de Valdo: analisar o
`D:\Gestao2027\setes-app\apps\web` e replicar o modelo do painel no
`apps/admin`. Análise de gap e plano executivo:
[plano-painel-modelo-setes.md](../plans/plano-painel-modelo-setes.md).
O que o VGR já tem a mais (privilégio por botão + enforcement no backend,
2FA, guarda 133, testes de wiring de rota, erro por código) fica.

215. **Shell persistente com duas colunas, igual ao setes.** Após o
     login, `HomeModule` desenha AppBar (título, seletor de idioma,
     badge do usuário com **Sair**) e corpo `módulos (200) | interfaces
     do módulo selecionado (240) | RouterOutlet`; abaixo de 850 px o
     menu vira drawer com grupos expansíveis. Seleção por clique, nunca
     hover. Páginas dentro do shell não desenham AppBar próprio
     (`VgrPage` no lugar do `VgrScaffold`; este fica para login/2FA).
     Logout limpa `LocalPrefs`, token do `ApiClient`, `SessionAccess`
     e `IdentityBloc`, e volta a `/login`.

216. **URLs das telas continuam na raiz** (`/reports`, `/users`…): o
     shell é montado em `/` e as `ModuleRoute` passam a ser filhas do
     `HomeModule`, sem `/home/...`. `interface_routes.dart`, bookmarks e
     testes de rota não mudam. Rotas de autenticação ficam fora do shell.

217. **CRUD simples alterna lista ↔ formulário por ESTADO do bloc**, numa
     só `ChildRoute('/')` por módulo (modelo setes: estados *buildable*
     `ListState`/`FormState` + *one-shot* `ActionSuccess`/`ActionFailure`).
     **Exceção registrada**: `reports` (`/:id`, `/queue`) e `admin-audit`
     (`/:id`) mantêm rota própria — deep link e leitura auditada por caso.

218. **`RouterOutlet` (flutter_modular) e o helper de breakpoint
     (`VgrResponsive`) são peças estruturais isentas da 133**, como
     `Navigator`/`BlocBuilder`; o ADR do design system lista ambos. O
     `vgr_widgets` não passa a depender de `flutter_modular`.

219. **Os motores do ERP ficam FORA**: campos configuráveis por
     instituição, configurações de interface e tema/logo por instituição
     não têm onde se encaixar numa instalação por país single-schema (68)
     com telas de governança. Registrado como visão futura, sem código.
     Também fora: seleção de instituição, `TreeView` e lookup de FK (até
     surgir a primeira tela que precise).

220. **Paginação obrigatória nas listas do painel que crescem** (usuários,
     privilégios, interfaces, módulos, Legal Gate, respondedores):
     `page`/`pageSize` (padrão 20, máximo 100) + `filter` opcional na API,
     envelope `{ items, page, pageSize, total }`; **sem `page` informado a
     API devolve tudo como hoje** (compatível até a migração das telas).
     Catálogos fixos (`risk-config` por categoria, `category-forms`)
     ficam sem paginação, registrado. `PagedResult<T>` no `core`,
     `VgrPagingBar` único no lugar dos controles duplicados.

221. **Ponte única de feedback verificada por teste**: telas chamam só
     `showSuccessFeedback`/`showFailureFeedback`/`showValidationFeedback`/
     `askDecision` de `app/shared/feedback`; `showVgr*` direto em tela
     passa a ser proibido pela mesma mecânica da 133 (teste que varre
     `apps/admin/lib`). Severidade derivada do `Failure`, nunca escolhida
     por tela.

222. **Fatiamento: PS0 API (paginação) ‖ PS1 shell → PS2 fábrica
     (`shared/register`, `shared/feedback`, `shared/session`,
     `VgrFormShell`, piloto `privileges` + `users`) → PS3 migração dos
     demais módulos → PS4 docs.** PS0 e PS1 em paralelo; PS2 só com as
     duas limpas (método 2026-09-04); cada fase por "pode seguir" (38).

     **Rodada 17 ZERADA** (decisões 215–222).

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
