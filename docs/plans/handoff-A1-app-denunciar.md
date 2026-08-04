# Handoff — A1 (app: denunciar) — sessão 2026-08-04

> Estado: A1 **INICIADO e PAUSADO** (prioridade desviada para o Gestão 2027).
> O lado API do A1 está PRONTO; o lado Flutter não tem código ainda.
> Este handoff destila o levantamento feito para a próxima sessão começar
> direto no código.

## O que já foi feito (commits)

- **R4 (mídia M2) EXECUTADA** — `api` commit `06dc960`; detalhes no
  plano-denuncia.md (seção 4) e `api/docs/feature/{reports,media}.md`.
- **Catálogo de formulários para o app** — `api` commit `72d098f`:
  `GET /app-reports/category-forms` (anônimo, todas as categorias numa
  leitura — o app cacheia localmente para renderizar/pré-validar offline;
  decisão 47). 54 suítes / 357 testes verdes.

## Plano de execução do A1 (tarefas definidas na sessão)

1. Bootstrap do `apps/mobile` (hoje é o scaffold do contador): `lib/app/`
   com AppModule/AppWidget espelhando `apps/admin`, main com
   EasyLocalization, translations pt-BR/en-US.
2. `OfflineQueueService` em `packages/core` (decisão 28): clientKey UUID
   gerado no ENQUEUE (idempotência 137), flush em ordem ao voltar
   conectividade, estados visíveis (queued/sending/sent/failed).
3. Módulo `report` (domain/data): ReportEntity (category XOR freeTag +
   subject obrigatório — 140), taxonomia espelhando os 12/9 da API,
   repository contra `/app-reports` + fallback para a fila.
4. Bloc + ReportFormPage: dois eixos obrigatórios ("other" de um toque),
   campos dinâmicos do schema cacheado, posição, escolha de anonimato
   (32), estado one-shot "queued offline"; só widgets `Vgr*` (133).
5. Captura: foto → re-encode JPEG no cliente (HEIC nunca viaja — emenda
   M1), diálogo EXIF v1 por foto (texto aprovado na decisão 139 +
   variante anônima; versão `exif-warning/v1`), upload `/app-media` +
   attach `/app-reports/:id/media` pela fila.
6. Testes (TDD, mocktail, sem bloc_test) + docs + commits.

## Levantamento do workspace Flutter (o que a próxima sessão precisa saber)

**Lacunas a fechar antes/junto do A1** (nada disso existe):

- `ApiClient` (packages/core/src/network) não tem **multipart** (upload) e
  renova token via `/api/auth/renew` (plano do PAINEL) — para o plano
  `/app-*` manter a instância **sem token** (anônimo) ou tratar renovação
  própria; erro 451 já tem view pronta (`LegalBlockedView.matches`).
- `OfflineQueueService` NÃO existe; sem connectivity_plus, sem
  image_picker/camera, sem geolocator, sem flutter_secure_storage, sem
  path_provider — adicionar deps conforme necessário.
- `packages/vgr_validators` é scaffold vazio.
- `vgr_widgets`: catálogo real = VgrPrimaryButton/Secondary/Text/Icon,
  VgrTextField (SEM onChanged/maxLines — precisa evoluir p/ descrição
  multilinha), VgrDropdownField, VgrGap/Column/Row/Padding/ScrollView/
  Expanded/ListView/StatefulContent, VgrText(.headline/.title/.caption/
  .error), VgrIcon (SEM ícone de câmera/foto/anexo — adicionar),
  VgrScaffold, VgrListTile/Checkbox/Switch/ExpansionTile/VgrCard,
  VgrLoading/InlineProgress, VgrMenuButton, showVgrConfirm/TextPrompt/
  Dialog/Message. NÃO existe VgrTokens (tema vem do ambiente).
- Guard do design system (`design_system_guard_test.dart`) só varre
  `apps/admin` + `packages/core` — criar equivalente em `apps/mobile`.
- Molde de módulo = `apps/admin/modules/category-forms` (Module com
  binds/rotas, entity Equatable+fromJson, repository → Either<Failure,T>
  via `on Failure catch`, bloc sealed states, page com switch exaustivo,
  keys em elementos interativos). Admin NÃO tem camada usecase; a spec
  mobile PREVÊ usecases — decidir deliberadamente (recomendação: seguir a
  spec mobile, com usecase).
- i18n: easy_localization, `assets/translations/{en-US,pt-BR}.json` por
  app (mobile só tem `app_name`), chaves nos DOIS na mesma edição.
- Testes: mocktail + `expectLater(bloc.stream, emitsInOrder)`;
  `pumpLocalized` helper do admin lê JSON do disco (copiar p/ mobile).
  Pisos de cobertura no ADR TESTS.md (domain 90 / data 80 / bloc 80).

## Depois do A1

A2 (feed + detalhe/timeline com posição degradada 135) → A3 (oferecer
ajuda) → P1 (tela mínima do congelamento no painel). Liberação fase a
fase segue com o Valdo (decisão 38).
