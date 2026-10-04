# Plano — Painel admin no modelo do setes-app (`apps/web`)

> **Rodada 17 — FECHADA em 2026-09-21** (aberta e zerada no mesmo dia).
> Pedido de Valdo: "analise como o painel admin do
> `D:\Gestao2027\setes-app\apps\web` é feito e replique o mesmo modelo
> neste projeto — plano antes de codar". Decisões **215–222** registradas
> no [VGR-plano.md](../decisions/VGR-plano.md) (respostas de Valdo às 8
> perguntas do §6: 1 duas colunas · 2 URLs na raiz · 3 lista↔form por
> estado · 4 RouterOutlet/Responsive isentos da 133 · 5 motores do ERP
> fora · 6 paginação obrigatória exceto catálogos fixos · 7 ponte de
> feedback por teste · 8 PS0 ‖ PS1). **PS0 e PS1 liberadas em 2026-09-21**
> ("pode seguir"). **PS1 shell EXECUTADA em 2026-09-21** (app: HomeModule
> como shell com RouterOutlet, duas colunas, drawer < 850, `UserBadge` +
> Sair, `VgrPage` nas 21 páginas, MenuBloc com seleção; `/welcome` e
> `/pending` sem barra final — regra do flutter_modular 5.0.3; hash no log
> do git). **PS0 API EXECUTADA em 2026-09-21** (api `cecc1e0`: `page`/
> `pageSize`/`filter` opcionais em privilégios, interfaces, módulos,
> usuários, Legal Gate e fila de respondedores; sem `page` a resposta é
> idêntica à anterior; helper único `shared/http/paged-query.ts`; 1204
> testes verdes). **PS2 liberada em 2026-10-04** ("pode seguir").
> **PS2 fábrica EXECUTADA em 2026-10-04** (app `f7ebbd7`: `PagedResult`/
> `PagedQuery` no core; `VgrFormShell`/`VgrPagingBar`/`VgrSearchBar`/
> `VgrEmptyState` + `showVgrAlert`/`showVgrChoice`; `shared/register`
> com `RegisterBloc<T, D>` genérico, `shared/feedback` e
> `shared/session/current_interface.dart`; piloto `privileges` + `users`;
> guarda da 221 com `interfaces`/`system-modules` na lista de pendência
> da PS3; admin 359 testes verdes — notas de execução no §7). **PS3
> liberada em 2026-10-04** ("pode seguir"). **PS3 migração EXECUTADA em
> 2026-10-04** (app `80cf51d`…`86fe644`, um commit por grupo de módulos:
> extensão da fábrica com a metade "lista paginada" para fluxos;
> `interfaces`/`system-modules` na fábrica; Legal Gate e fila de
> respondedores paginados; catálogos fixos, fluxos, detalhe/fila de
> moderação na ponte; um `PagedResult` e um `VgrPagingBar` para tudo;
> guarda da 221 estrita, sem lista de pendência; admin 387 testes verdes —
> notas no §8). **PS4 docs aguarda "pode seguir".** Execução fase a fase
> (38).

---

## 1. Como o painel do setes é feito (referência)

Fontes: `apps/web/lib/app/{app_module,app_widget}.dart`,
`modules/home/*`, `modules/banks/*` (CRUD mínimo), `modules/customers/*`
(agregado com abas), `lib/app/shared/*`, `packages/{core,setes_widgets}`,
e a especificação `D:\Gestao2027\Infra-IA\setes-app\ARQUITETURA_MODULOS.md`.

### 1.1 Shell persistente pós-login
- `AppModule` tem só duas rotas: `ModuleRoute('/', AuthModule())` e
  `ModuleRoute('/home', HomeModule(), guards: [SetesAuthGuard()])`.
- `HomeModule` é o **shell**: `ChildRoute('/')` desenha a `HomePage` e
  **todas as interfaces são `ModuleRoute` filhas** (`/home/customers/`,
  `/home/banks/`…), renderizadas dentro de um `RouterOutlet()` no corpo.
- `HomePage` → `Responsive(mobile:, desktop:)` (breakpoints 850/1100):
  - **Desktop** (`content_home_desktop.dart`): `SetesScaffold` com AppBar
    (logo, `UserBadge` com **Sair**, `LanguageSelector`, tema) e corpo
    `Row[ coluna de módulos 200px | coluna de interfaces do módulo
    selecionado 240px | Expanded(RouterOutlet) ]`. Seleção destacada via
    `SetesListTile(selected:)` ligada ao `MenuBloc`
    (`selectedModuleIndex`/`selectedInterface`). Clique, nunca hover.
  - **Mobile**: mesmos dados num `Drawer` com `ExpansionTile`; corpo é o
    `RouterOutlet`.
- `/home/welcome/` é o conteúdo padrão; `/home/pending/` é o fallback de
  interface catalogada sem tela.

### 1.2 Menu dinâmico e registro de tela
- `GET /api/core/menus` → `MenuModule{id?, description, icon, interfaces}` /
  `MenuInterface{id, description, i18nKey, privileges}`, já filtrado pelo
  backend. `MenuBloc` guarda a seleção (módulo/interface).
- `interface_routes.dart`: `Map<i18nKey, rota>` + `navigateToInterface`,
  que grava `CurrentInterface.value` (privilégios da tela aberta) e navega
  passando o **título traduzido como `arguments`** — a página usa esse
  título no AppBar (é o "breadcrumb").
- Contrato de registro de tela: **1 entrada em `interfaceRoutes` + 1
  `ModuleRoute` no `home_module.dart`**. "1 interface = 1 módulo
  flutter_modular"; módulo de sistema (agrupador do menu) nunca é pasta.

### 1.3 Anatomia do CRUD (a "fábrica")
- Pasta por módulo: `data/{datasource,repository}`,
  `domain/{entity,repository,usecase/<x>_{getlist,post,put,delete}}`,
  `presentation/{bloc,page}`. Módulo nunca importa módulo; 2+ consumidores →
  `app/shared/` (negócio) ou `packages/` (infra/design).
- **Um bloc por módulo alterna lista ↔ formulário por ESTADO**
  (`BankListState` / `BankFormState`, eventos `NewPressed`, `EditPressed`,
  `BackToListPressed`, `SaveRequested`, `DeleteRequested`); estados
  *buildable* separados dos *one-shot* `ActionSuccess(messageKey)` /
  `ActionFailure(failure)` consumidos só no `listener`. **Uma só
  `ChildRoute('/')` por módulo** — a URL não muda entre lista e form.
- `app/shared/register/`:
  - `RegisterSearchPage<T>` — AppBar (título + ações + engrenagem), campo
    de filtro (Enter/ícone), FAB "novo", `ListView.separated` de
    `SetesListTile` (`avatarBuilder`/`rowBuilder`), vazio =
    `register.emptyList`, rodapé `RegisterPagingBar` quando
    `page/pageSize/total/onPageChanged` vêm preenchidos.
  - `RegisterFormPage` — recebe `List<RegisterField>` (nome, label,
    readOnly, teclado, validator, máscara, hint, lookup), monta
    `SetesTextField`s num `Form` com ordem de Tab = ordem de declaração,
    Enter avança/submete; **valida uma pendência por vez** (dialog na
    primeira, nunca pinta o form todo); `showServerFieldError(failure)`
    ancora `fields[]` de 400/409 no campo certo (trocando de aba antes se
    preciso); `extraTabs` vira `TabBar`.
  - `RegisterPagingBar` (persiste o page-size escolhido),
    `RegisterConfigButton`, `applyFieldConfig`.
- `SetesFormShell` (widget): AppBar com voltar / título / salvar / excluir.
- `app/shared/feedback/`: **ponte única** `showSuccessFeedback`,
  `showFailureFeedback`, `showValidationFeedback`, `askDecision`
  (sim/não/cancelar tipado); telas nunca chamam `ScaffoldMessenger` ou
  `AlertDialog`. Severidade derivada do `Failure` (técnico → dialog com
  código de suporte; sucesso → SnackBar).
- **Paginação obrigatória** em lista nova (`PagedResult<T>` no core).
- Exclusão sempre por `askDecision` antes do evento.
- Agregados complexos (customers): form à mão com abas compartilhadas de
  `shared/entity/widgets`, *draft* inteiro no bloc, `copyWith` por aba,
  `PendencyField` com `beforeFocus` para trocar de aba.

### 1.4 Sessão
- `AuthModule` inteiro vive em `packages/core` (reutilizável por outros
  apps). `SetesAuthGuard` reidrata o JWT do `LocalPrefs`. `UserBadge`
  (`GET /api/core/me`) mostra o usuário e oferece **Sair** (limpa prefs,
  tema, token; volta a `/login`). `SessionContext` (ChangeNotifier) guarda
  fatos da sessão e é reidratado ao entrar na Home. Sem 2FA.

### 1.5 Motores de configuração (ERP)
- "Campos configuráveis" (`field_config`: caption/required/mask por
  instituição) e "Configurações de interface" (`interface_config`: toggles
  de negócio), ambos com engrenagem na lista. Tema por instituição via
  `ThemeCubit` + `GET /api/core/theme`.

## 2. Como está o painel do VGR hoje

Fontes: `apps/admin/lib/app/**`, `packages/{core,vgr_widgets}`,
`app/docs/adr/*.md`, `app/docs/feature/admin-panel.md`.

| Dimensão | setes `apps/web` | VGR `apps/admin` hoje |
|---|---|---|
| Shell | persistente (AppBar + 2 colunas + `RouterOutlet`), responsivo | **não existe** — cada página monta o próprio `VgrScaffold` com AppBar; `AppWidget` entrega direto ao router; 16 `ModuleRoute` irmãs na raiz |
| Menu | 2 colunas com seleção destacada; drawer no mobile | lista de `VgrExpansionTile` numa página `/` que é abandonada ao navegar; volta só pelo botão do navegador (ou `/pending`) |
| Sair / usuário | `UserBadge` + Sair | **não existe logout** em lugar nenhum (blocos prontos: `LocalPrefs.clearSession`, `ApiClient.setToken`) |
| Responsividade | `Responsive` 850/1100, arquivos `content_*_desktop/mobile` | nenhuma (`VgrWrap` pontual) |
| Menu dinâmico | `GET /api/core/menus`, `MenuBloc` com seleção | igual na origem (`core/menu`, decisão 71), **sem estado de seleção**; `SessionAccess.can()` alimentado por `GET /api/core/permissions` — VGR tem a mais o `can()` por botão e o enforcement no backend (72) |
| Registro de tela | `interfaceRoutes` + `ModuleRoute` no `home_module` | `interfaceRoutes` + `ModuleRoute` no **`app_module`**; título não viaja como `arguments` |
| CRUD | fábrica `RegisterSearchPage`/`RegisterFormPage`/`SetesFormShell`; lista↔form por estado do bloc | cada tela à mão: `users` abre form em **dialog** sem `vgr_validators`; `privileges`/`interfaces`/`system-modules`/`risk-config`/`monetization` listam tudo sem filtro nem paginação; `reports`/`admin-audit` paginam com controles **duplicados byte a byte** |
| Paginação | obrigatória, `PagedResult<T>`, `RegisterPagingBar` | só `reports` e `admin-audit` na API; core sem `PagedResult`; sem widget |
| Feedback | ponte única `shared/feedback` | `showVgrConfirm/showVgrDialog/showVgrMessage` chamados direto por tela; `failureText` por código (80/83) já existe |
| Validação | `SetesValidators` + uma pendência por vez + âncora de erro do servidor | `VgrValidators.validate` em `reports`/moderação; `users` só `isNotEmpty` |
| `app/shared` | rico (register, feedback, session, lookup, entity) | **não existe** no admin (ADR documenta, só o mobile tem) |
| Design system | `Setes*` sem i18n/API | `Vgr*` + **guarda por teste** (133) — VGR está à frente |
| Sessão | guard reidrata; sem 2FA | guard reidrata + renovação silenciosa + **2FA obrigatório** (114) — à frente |
| Testes | unitários de entidade/bloc, poucos de widget | 55 arquivos, testes de página, guarda 133, `admin_module_wiring_test` (rotas reais) — à frente |
| Tema | por instituição (`ThemeCubit`) | fixo (coerente com 68: instalação por país, single-schema) |

O que o VGR tem **a mais** e deve ser preservado: privilégio por botão
(`SessionAccess.can`, 72), 2FA (114), auditoria de leitura (116/166),
guarda do design system (133), testes de wiring de rota, erro por código
(80/83), i18n por catálogo (`trCatalog`).

## 3. Proposta

Replicar o **modelo** (shell + contrato de registro + fábrica CRUD +
ponte de feedback + paginação obrigatória), não o produto ERP. Ficam de
fora, por não haver equivalente no VGR: campos configuráveis,
configurações de interface, tema/logo por instituição, seleção de
instituição, `SetesTreeView`, lookup de FK (não há campo FK em tela do
painel hoje).

### 3.1 Shell (fase PS1)
- `HomeModule` vira o shell: `ChildRoute('/')` com `VgrAdminShell`;
  **as 16 `ModuleRoute` saem do `AppModule` e entram como filhas do
  `HomeModule`**. Com o `HomeModule` montado em `/`, as URLs atuais
  (`/reports`, `/users`…) **não mudam** — `interface_routes.dart` fica
  igual, bookmarks e testes de rota continuam válidos. Rotas de auth
  (`/login`, `/recovery-password`, `/change-password`, `/two-factor-*`)
  permanecem no `AppModule`, fora do shell.
- Layout desktop = setes: AppBar (título do app, `LanguageSelector`,
  **`VgrUserBadge` com Sair**) + `Row[ módulos 200 | interfaces 240 |
  Expanded(RouterOutlet) ]`. Mobile (< 850): `VgrDrawer` com grupos
  expansíveis + `RouterOutlet`. `/welcome` como conteúdo padrão (hoje o
  `/` mostra o menu; passa a mostrar boas-vindas dentro do outlet);
  `/pending` continua.
- `MenuBloc` (core) ganha `MenuModuleSelected`/`MenuInterfaceSelected` e
  os campos de seleção no `MenuLoaded`; `navigateToInterface` passa a
  também gravar a interface corrente (`CurrentInterface` em
  `app/shared/session/`) e a levar o **título como `arguments`**.
- Logout: `VgrUserBadge` lê `GET /api/core/me` (já existe na API) e o
  "Sair" limpa `LocalPrefs.clearSession`, `ApiClient.setToken(null)`,
  `SessionAccess.clear()`, reseta `IdentityBloc` e navega a `/login`.
- Páginas dentro do outlet **não podem ter AppBar próprio** (ficaria
  duplo). Novo widget `VgrPage(title, actions, body)` (cabeçalho de
  conteúdo) substitui o `VgrScaffold` nas ~20 páginas do admin; o
  `VgrScaffold` continua para as telas fora do shell (login/2FA). Troca
  mecânica, uma página por commit ou em lote — decisão de granularidade na
  execução.
- Widgets novos em `vgr_widgets`: `VgrResponsive` (850/1100),
  `VgrSideMenu`/`VgrMenuColumn` (coluna com `selected`), `VgrDrawer`,
  `VgrPage`. `RouterOutlet` (flutter_modular) entra na lista de peças
  estruturais isentas da 133 (como `Navigator`/`BlocBuilder`) — o
  `vgr_widgets` não deve depender de `flutter_modular`.
- Testes: `admin_module_wiring_test` passa a montar o shell real e cobrir
  **todas** as rotas (hoje só as 5 da fase 1); teste do shell (colunas,
  seleção, drawer no mobile via `tester.view.physicalSize`, Sair);
  guarda 133 recebe as isenções novas.

### 3.2 Fábrica CRUD (fase PS2) — `apps/admin/lib/app/shared/`
- `core`: `PagedResult<T>{items, page, pageSize, total}` espelhando o
  envelope que `reports`/`admin-audit` já devolvem.
- `vgr_widgets`: `VgrFormShell` (voltar/título/salvar/excluir),
  `VgrPagingBar` (anterior/próxima/"página X de Y"/tamanho), `VgrSearchBar`
  (campo de filtro com Enter/ícone), `VgrEmptyState`.
- `shared/register/`: `RegisterSearchPage<T>` (filtro, FAB por
  privilégio INSERT, lista, vazio, paginação), `RegisterFormPage` +
  `RegisterField` (ordem de Tab, máscara via `VgrTextField.mask`,
  validação **uma pendência por vez** com `vgr_validators`,
  `showServerFieldError` para `Failure.fields`), `RegisterFormState`
  base.
- `shared/feedback/`: `showSuccessFeedback`, `showFailureFeedback`
  (severidade pelo `Failure`: `statusCode >= 500` → dialog com
  `supportRef` se houver; senão SnackBar/dialog conforme setes),
  `showValidationFeedback`, `askDecision` (sim/não/cancelar) — todos por
  cima de `showVgr*`. Telas deixam de chamar `showVgr*` direto (regra
  nova, verificável por teste como a 133).
- `shared/session/current_interface.dart`.
- Padrão de bloc para CRUD: `ListState`/`FormState` *buildable* +
  `ActionSuccess`/`ActionFailure` *one-shot*; lista↔form por estado numa
  só `ChildRoute('/')`. **Exceção registrada**: `reports` (`/:id`,
  `/queue`) e `admin-audit` (`/:id`) mantêm rota própria — deep link e
  leitura auditada por caso.
- Piloto: `privileges` (CRUD mais simples) e depois `users` (form sai do
  dialog; senha inicial; `fields[]` do servidor ancorados; `SELF_LOCKOUT`
  pela ponte).

### 3.3 Paginação na API (fase PS0, **antes** da PS2 — método API primeiro)
Listas do painel sem `page/pageSize` hoje: `privileges`, `interfaces`,
`system-modules`, `users`, `risk-config`, `monetization-config`,
`legal-policy` (3 recursos), `panic-responders` (fila),
`category-forms`. Proposta: DTO comum `pagedQueryDto{ page=1,
pageSize=20 (max 100), filter? }` em `shared/http/`, envelope
`{ items, page, pageSize, total }`; **sem página informada, devolve tudo
como hoje** (compatibilidade com o app atual até a PS3). Spec 004 emendada.
Categorias fixas (`risk-config`, `category-forms`: 5–10 linhas) podem
ficar sem paginação por decisão explícita — pergunta 6.

### 3.4 Migração das telas (fase PS3)
Ordem sugerida, um commit por módulo, cada um trocando para a fábrica e
para `VgrPage`: `interfaces` → `system-modules` → `users` (com
`UserPrivilegesPage` mantida como aba/rota) → `legal-policy` (3) →
`monetization-config` → `panic-responders` → `risk-config`/
`category-forms` (só `VgrPage` + feedback, sem paginação se a pergunta 6
disser que não) → `dual-control-access`/`case-freeze`/`reward-mediation`
(fluxos, só `VgrPage` + ponte) → `reports`/`admin-audit`/`report-stats`
(`VgrPage`, `VgrPagingBar` no lugar dos controles duplicados, ponte de
feedback).

### 3.5 Documentação (fase PS4)
`ARCHITECTURE.md` (seção admin: shell, contrato de registro, fábrica,
exceções), `DESIGN-SYSTEM.md` (isenções `RouterOutlet`/`Responsive`,
widgets novos), `TESTS.md` (wiring de rota obrigatório para módulo novo),
`admin-panel.md` (reescrito), checklist "nova tela no painel" (espelho do
`ARQUITETURA_MODULOS.md` do setes). `VGR-RESUMO.md` §4 ganha a linha da
frente.

## 4. Fatiamento e ordem
| Fase | Conteúdo | Depende de |
|---|---|---|
| **PS0 API** | paginação nas listas do painel (compatível), spec 004 | rodada 17 | ✅ 2026-09-21 (`cecc1e0`) |
| **PS1 shell** | HomeModule shell + RouterOutlet + colunas + drawer + Sair + `VgrPage` em todas as páginas + MenuBloc com seleção + testes | rodada 17 | ✅ 2026-09-21 |
| **PS2 fábrica** | `PagedResult`, `VgrFormShell`/`VgrPagingBar`/`VgrSearchBar`/`VgrEmptyState`, `shared/register`, `shared/feedback`, `shared/session`; piloto `privileges` + `users` | PS0, PS1 | ✅ 2026-10-04 (`f7ebbd7`) |
| **PS3 migração** | demais módulos na fábrica/ponte, dedupe de paginação | PS2 | ✅ 2026-10-04 (`80cf51d`…`86fe644`) |
| **PS4 docs** | ADRs, feature doc, checklist, resumo | PS3 |

PS0 e PS1 são independentes e podem correr em paralelo (sessões
distintas, claim na memória). PS1 é a maior entrega visível: ~20 páginas
trocam `VgrScaffold` por `VgrPage`.

## 5. Critérios de sucesso
1. Após o login, o usuário vê AppBar + colunas de módulos/interfaces e o
   conteúdo troca dentro do outlet sem perder o menu; a URL de cada tela
   é a de hoje.
2. "Sair" existe, limpa a sessão e volta ao login; F5 numa tela interna
   reidrata a sessão (guard) e reabre a mesma tela dentro do shell.
3. Em largura < 850 o menu vira drawer.
4. Nenhuma página dentro do shell desenha AppBar próprio (teste).
5. `privileges` e `users` usam a fábrica: filtro, paginação, FAB por
   INSERT, form com validação uma pendência por vez, erro de campo do
   servidor ancorado, exclusão por `askDecision`.
6. Nenhuma tela chama `showVgr*` direto (teste, mesma mecânica da 133).
7. `admin_module_wiring_test` cobre todas as rotas do shell; suíte do
   admin e guarda 133 verdes; API verde.

## 6. Perguntas da rodada 17 — RESPONDIDAS em 2026-09-21 (decisões 215–222; recomendações aceitas em todas)
1. **Layout do shell**: replicar as duas colunas do setes (módulos |
   interfaces) ou uma barra lateral única com grupos expansíveis?
   *Recomendação*: duas colunas, é "o mesmo modelo".
2. **URLs**: manter as atuais na raiz (`/reports`) com o shell em `/`, ou
   mover tudo para `/home/...` como no setes? *Recomendação*: manter —
   zero mudança em `interfaceRoutes`, bookmarks e testes.
3. **Lista ↔ formulário por estado do bloc** (setes, URL fixa) para os
   CRUDs simples, com `reports`/`admin-audit` mantendo rota própria?
   *Recomendação*: sim.
4. **`RouterOutlet` e `Responsive` como peças estruturais isentas da 133**
   (ADR) em vez de encapsular em `core`? *Recomendação*: isentar.
5. **Motores do ERP fora** (campos configuráveis, configurações de
   interface, tema/logo por instituição)? *Recomendação*: fora; registrar
   como visão futura, sem código.
6. **Paginação obrigatória** vale para todas as listas do painel, ou
   catálogos fixos pequenos (`risk-config` por categoria, `category-forms`)
   ficam sem? *Recomendação*: obrigatória para o que cresce (usuários,
   privilégios, interfaces, módulos, legal, respondedores); catálogos
   fixos ficam sem, registrado.
7. **Ponte de feedback verificada por teste** (proibir `showVgr*` direto
   em tela, como a 133 proíbe widget cru)? *Recomendação*: sim.
8. **Ordem**: PS0 (API) e PS1 (shell) em paralelo, PS2 depois de ambas?
   *Recomendação*: sim.

## 7. Notas de execução da PS2 (2026-10-04)

Escolhas de implementação dentro das decisões 215–222 — nenhuma decisão
nova; registradas para a PS3/PS4 não as redescobrirem.

1. **Bloc genérico em vez de um bloc à mão por módulo.** `RegisterBloc<T, D>`
   (entidade, rascunho) faz o ciclo lista ↔ formulário da 217 uma vez; o
   módulo declara o seu como alias (`typedef PrivilegeBloc =
   RegisterBloc<PrivilegeEntity, PrivilegeDraft>`) e implementa
   `RegisterRepository<T, D>` (lista paginada + criar/alterar/excluir). A
   tela é `RegisterScreen<T, D>` + configuração. Setes tem um bloc por
   módulo; aqui a PS3 migra ~6 CRUDs sem repetir os estados.
2. **`CurrentInterface` por chave, não global.** No setes a navegação
   grava a interface corrente num global; no VGR o `MenuBloc` do shell já
   guarda a seleção (PS1) e um global ficaria velho num F5 ou deep link.
   Cada tela passa a sua `i18n_key`; a resposta vem do `SessionAccess`.
3. **Título NÃO viaja como `arguments`** (§3.1 previa): cada página
   mantém a sua chave de tradução — mesma informação, sem depender de ter
   chegado pelo menu.
4. **Severidade da ponte (221)**: sem status (sem resposta) ou 5xx →
   dialog; 4xx → mensagem transitória, sempre traduzida por código. A API
   não devolve código de suporte (`supportRef`), então o dialog técnico
   mostra só o texto traduzido.
5. **Guarda da 221 com catraca**: `interfaces` e `system-modules` (as duas
   telas que ainda chamam `showVgr*`) ficam numa lista de pendência que
   só encolhe — um segundo teste falha se um arquivo listado deixar de
   ofender. A PS3 esvazia a lista; `change_password_page` e
   `user_privileges_page` já passaram para a ponte nesta fase.
6. **Exclusão mora no formulário** (como `SetesFormShell`), não mais num
   ícone por linha; sem UPDATE a linha abre o formulário só leitura, para
   o registro continuar consultável.
7. **Validadores novos** (espelhos da 154): `upperSnakeCase`
   (`privilegeSaveDto`), `newPassword` (só o comprimento de
   `newPasswordSchema`, sem trim; o refine "senha previsível" fica só na
   API e volta como 422 no campo `password`, ancorado pelo formulário) e
   `optional(rule)`.
8. **Achado — `locale` apagado ao editar usuário**: a API grava `locale`
   em todo `PUT /api/users/:id` e trata ausente como `null`; o painel
   nunca enviava, então editar o nome de alguém zerava o idioma salvo.
   Corrigido no app (o update reenvia o `locale` atual). **Pendente de
   decisão de Valdo**: se a API deve passar a preservar o valor quando o
   campo não vem (hoje o DTO não distingue ausente de `null`).
9. **Tamanho de página não é persistido** (o setes persiste): vale durante
   a vida da tela. Entra se fizer falta no uso.

## 8. Notas de execução da PS3 (2026-10-04)

Dentro das decisões 215–222; nenhuma decisão nova. Onde a execução se
afastou do §3.4, o motivo está aqui.

1. **Legal Gate e fila de respondedores não são CRUDs** (o §3.4 os punha
   na fábrica): kill switch, regra versionada com aprovação por outra
   pessoa, aprovar/negar fila. Ganharam só a METADE LISTA da fábrica —
   `PagedListBloc<T>` (consulta, última página, recarga silenciosa e
   `act()`: ação de linha → sinal para a ponte → recarga silenciosa, o
   servidor dá a palavra final) + `PagedListScreen`. `RegisterBloc` passou
   a estender `PagedListBloc` (sem mudança de comportamento).
2. **Regras do Legal Gate**: fábrica com formulário só de PROPOSTA (regra
   é versionada — mudança é proposta nova, 107), linhas que não abrem,
   aprovar/rejeitar na linha. O motivo aparece e vira obrigatório só para
   status diferente de `allowed` (78) e **não vem pré-selecionado** (antes
   vinha `no_control`) — obrigar a escolha explícita. Os dois filtros
   exatos (capacidade, jurisdição) viraram o filtro de texto da API
   (capacidade / código / base legal).
3. **Capacidades**: a jurisdição continua sendo digitada no cabeçalho;
   nada é buscado antes dela (o vazio diz o que falta).
4. **Campos novos na fábrica**: escolha (dropdown), checklist (com
   `ordered` = ordem do clique, usado na ordem do menu dos módulos) e
   `visibleWhen`; catálogos pequenos de opções carregam uma vez ao lado da
   lista (`RegisterLookupCubit`, forma sem paginação da API, que a 220
   mantém para isso).
5. **Telas de fluxo** (dual-control, case-freeze, reward-mediation,
   detalhe do caso, fila de moderação) e **catálogos fixos** mantêm blocs
   próprios; o resultado das ações passa pela ponte a partir de um
   listener. Erros de busca/carga continuam como estado da tela.
6. **Paginação deduplicada**: `ReportPageEntity`, `QueuePageEntity` e
   `AuditPageEntity` (três cópias do mesmo envelope) viraram aliases de
   `PagedResult<T>`; os três pagers feitos à mão viraram `VgrPagingBar`.
7. **Defeitos achados e corrigidos de passagem** (todos com teste):
   - fila de respondedores, risk-config, category-forms e monetization:
     uma ação recusada trocava a tela inteira por erro, com o texto cru da
     API em inglês (contra 80/83) — agora a lista fica e a recusa vai
     traduzida pela ponte;
   - dual-control: uma aprovação recusada voltava ao formulário inicial e
     a solicitação em andamento sumia da vista — agora a tela fica no passo
     em que estava;
   - entradas obrigatórias ignoradas em silêncio (percentual de taxa fora
     de 0..100, base legal/ID do log no dual-control, versão/texto dos
     critérios de mediação) — agora viram a pendência do formulário;
   - tooltips de aprovar/negar respondedor diziam "Salvar"/"Cancelar".
8. **Mensagens de sucesso** novas onde antes não havia retorno nenhum
   (salvar tier, campo de categoria, regra de taxa, resolver respondedor).
9. **Catálogos de tradução**: 19 chaves por idioma sem uso removidas.
10. **Para a PS4**: além do previsto no §3.5, varrer os feature docs do
    app (`legal-policy.md`, `panic-responders.md`, `monetization-config.md`,
    `dual-control-access.md`, `case-freeze.md`, `admin-audit.md`) — ainda
    descrevem erros inline e filtros antigos; `report-moderation.md`,
    `ARCHITECTURE.md`, `TESTS.md` e `admin-panel.md` já foram ajustados.

## Fora de escopo (registrado, não some)
- Convite de equipe por e-mail (75), refresh token do painel (73).
- Lookup de FK e `TreeView` — entram quando surgir a primeira tela que
  precise.
- Mapa de calor (164), imagem autenticada no painel web (frente 142).
