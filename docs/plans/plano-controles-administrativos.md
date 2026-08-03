# Plano — Controles Administrativos do VGR

> Estruturar o VGR com o padrão do Gestão 2027 (setes-app / setes-api): controle de
> módulos e menus, permissão por usuário e internacionalização — adaptado à visão
> do VGR (instalação por país, sem licenciamento de interfaces, sem superusuário).
>
> Data: 2026-08-03 · Status: aprovado — decisões 68–75 registradas em
> `AI\docs\decisions\VGR-plano.md` (rodada 1; restam 2 assunções a confirmar)

---

## 1. Princípios (derivados da visão de produto)

| # | Princípio | Consequência estrutural |
|---|---|---|
| P1 | Cada país pode ter instalação própria (soberania de dados) | **Single-schema por instalação.** NÃO copiar o multi-tenant do setes: sem `schema_name`, sem `tb_institution`, sem interpolação de schema nas queries. O runner de migração atual do VGR já serve. |
| P2 | Não há venda por interface — tudo vai no pacote | **NÃO copiar `tb_institution_has_interface`** (contrato comercial). A visibilidade é decidida só por permissão de usuário. |
| P3 | Não há superusuário; o Admin administra permissões dos demais | **Sem `superGuard`/institution 1.** "Admin" deixa de ser um role mágico e vira um usuário com privilégio na interface de Usuários/Permissões. Bootstrap via seed. |
| P4 | VGR é produto de segurança pública | **Enforcement de privilégio no backend por endpoint** — divergência consciente do setes, onde `tb_user_has_privilege` só filtra o menu e a API não bloqueia ação fina. No VGR isso não é aceitável. |
| P5 | Utilizável por qualquer país | i18n desde já (en-US fonte, pt-BR primeira tradução), locale persistida por usuário, erros de API por código estável. |

Escopo deste plano: a **equipe administrativa** (apps/admin). Os papéis do app móvel
(`reporter`, `helper`, `police`) continuam no modelo de identidade atual e ficam fora
do sistema de privilégios — são usuários finais, não equipe.

---

## 2. Modelo de dados alvo (migrações 019+)

Copiado do setes com as simplificações P1–P3:

```
tb_user                      (evolução de tb_admin_account: + name, active, locale,
                              last_login_at, activation_key; senha continua bcrypt)
tb_privilege                 (seed: INSERT, UPDATE, DELETE, PRINT, VIEW — VIEW decide menu)
tb_interface                 (id, description, i18n_key, group_default, kind 'T'/'R', position)
tb_interface_has_privilege   (PK interface×privilege — quais ações a tela possui)
tb_module                    (menu do cliente: description, i18n_key, icon, position)
tb_module_has_interface      (PK module×interface — telas dentro do módulo)
tb_user_has_privilege        (PK user×interface×privilege — a concessão efetiva)
```

Cadeia: **usuário → concessão → interface → módulo/menu**. Sem camada de contrato.

Notas:
- Manter convenções já vigentes no VGR: prefixo `tb_`, soft delete `deleted='S'/'N'`
  (as tabelas novas já nascem com a coluna; as antigas ficam como estão).
- `tb_admin_account` → `tb_user`: migração renomeia/evolui preservando os admins
  existentes; seed concede a eles **todos** os privilégios (bootstrap do P3).
- Seed de `tb_interface`: registrar as 5 telas já existentes do admin
  (risk-config, category-forms, panic-responders, dual-control-access,
  monetization-config) + as novas telas administrativas da Fase 4.

---

## 3. Fases

### Fase 0 — Decisões (obrigatória antes de codar)
O VGR exige decisão numerada em `AI\docs\decisions\VGR-plano.md` (método
`decision-rounds`). Hoje vai até a 67. Registrar como 68+:

1. **Modelo de permissões** — módulo→interface→privilégio, sem contrato comercial,
   sem super (P1–P3 acima).
2. **Enforcement backend por endpoint** (`requirePrivilege`) — divergência
   consciente do setes (P4).
3. **Sessão persistente** — "manter logado" no admin + política de expiração
   (TTL 24h atual vs refresh token).
4. **i18n de erros da API** — fecha a pendência da decisão 17 (chave estável por
   `error-codes.ts`, tradução no cliente).

### Fase 1 — API: fundação de permissões ✅ CONCLUÍDA (2026-08-03)
- Migração `019_permission_model.sql` (tabelas da seção 2) + `020_seed_*.sql`.
- Módulos novos no padrão de 6 arquivos (`_template` já existe no VGR):
  - `privileges` — CRUD (porta direta de `setes-api/src/modules/privileges/`).
  - `interfaces` — CRUD + sincronização de `privilegeIds[]` (porta de
    `setes-api/src/modules/interfaces/`, sem a parte de configs se não for usada agora).
  - `modules` — CRUD de `tb_module` + `tb_module_has_interface`. **Código novo**:
    o setes nunca implementou esse endpoint (lacuna confirmada).
  - `users` — evoluir: CRUD de equipe + `GET/PUT /api/users/:id/privileges`
    (porta de `setes-api/src/modules/users/`, removendo institutionId/escopo).
  - `core` — `GET /api/core/menus` (porta simplificada de `core.service.getMenus`:
    único caminho = filtro por privilégio VIEW; sem ramo super/admin/contrato),
    `GET /api/core/me`, `GET/PUT /api/core/preferences` (locale).
- **`requirePrivilege(interfaceKey, privilege)`** middleware substituindo o
  `require-admin.middleware.ts` binário, aplicado rota a rota
  (GET→VIEW, POST→INSERT, PUT→UPDATE, DELETE→DELETE). JWT continua mínimo
  (`userId`); privilégios consultados no banco com cache TTL (padrão do
  `feature-flag.middleware.ts` do setes).
- Manter compatibilidade: enquanto o app não migra, `require-admin` e
  `requirePrivilege` convivem; a troca é rota a rota.

### Fase 2 — Auth completo (reuso do pacote setes) ✅ CONCLUÍDA (2026-08-03)
> Inclui o passo 1 da Fase 5 (EasyLocalization ativado e as 7 telas
> existentes traduzidas en-US/pt-BR antes das telas novas).
API (porta de `setes-api/src/modules/auth/` + `src/shared/mailer/`):
- `POST /auth/login` (bcrypt — já é assim no VGR; **não** levar o MD5 do setes),
  `POST /auth/recovery-password` (código 6 dígitos, janela 15 min, resposta
  genérica anti-enumeração), `POST /auth/change-password`.
- Rate-limit em `/auth` (lacuna atual do VGR — hoje só `/api` tem).
- Sem select-institution/switch-institution (P1: não há multi-empresa).

App (porta de `setes-app/packages/core/lib/src/auth/` para
`app/packages/core/lib/src/auth/`):
- `AuthModule` completo: LoginPage responsiva, recovery, change-password, AuthBloc.
- `LocalPrefs` (`shared_preferences` — já declarado no core do VGR, hoje inerte):
  `session_token` (persistido só com "Manter conectado"), `keep_connected`,
  `remembered_email` (nunca a senha).
- `jwt_utils.dart` + guard que restaura sessão no refresh do navegador
  (resolve a queda de sessão atual do admin).
- Substitui o par LoginBloc/admin_session_guard atuais.

### Fase 3 — Menu dinâmico ✅ CONCLUÍDA (2026-08-03)
- App: portar `setes-app/packages/core/lib/src/menu/` (entity/model/datasource/
  repository/usecase) para o core do VGR — `MenuModule`/`MenuInterface` com
  `i18nKey` e `can(privilege)`.
- Home: substituir o `_links` hardcoded de `home_page.dart` pelo menu vindo de
  `GET /api/core/menus` (padrão 2 colunas do setes ou layout próprio).
- `interface_routes.dart`: mapa central `i18nKey → rota` + rota `pending`
  para interface cadastrada sem tela (regra "criar módulo = 2 edições").
- **Cabear `MenuInterface.can()` nos botões** (novo/editar/excluir) — no setes
  esse gancho existe mas está morto; no VGR ele fecha o P4 no cliente
  (a API continua sendo a autoridade).

### Fase 4 — Telas administrativas (apps/admin) ✅ CONCLUÍDA (2026-08-03)
> Inclui a execução do `plano-erro-i18n.md` (decisões 80/83): códigos
> IN_USE/SELF_LOCKOUT/BUSINESS_RULE/NOT_AVAILABLE, HttpError.code
> obrigatório, fields[].code + params no zodToFields, e o app traduzindo
> por código (failureText/fieldFailureText no core).
No padrão 1 interface = 1 módulo (camadas + bloc), na ordem:
1. **Privilégios** — CRUD simples (molde: `modules/privileges` do setes).
2. **Interfaces** — CRUD + checkboxes de privilégios da tela.
3. **Módulos/Menu** — CRUD de `tb_module` + ordenação e vínculo de interfaces.
   Tela nova (não existe no setes); considerar `SetesTreeView` para a árvore
   módulo→interfaces.
4. **Usuários** — CRUD de equipe + aba "Privilégios de Acesso" (molde:
   `user_privileges_section.dart` do setes; manter a regra "marcar qualquer
   privilégio marca VIEW junto", mas por **descrição/constante nomeada**, não
   pelo id mágico 6).
- Avaliar portar a fábrica `RegisterSearchPage`/`RegisterFormPage` do setes para
  `apps/admin/lib/app/shared/register/` — paga o custo já na 1ª tela e padroniza
  as 4.

### Fase 5 — Internacionalização ✅ CONCLUÍDA (2026-08-03)
> Passo 1 (ativação + telas traduzidas) entrou junto com a Fase 2; o
> restante — LanguageSelector (login local-only, home persistindo via
> PUT /api/core/preferences) e applyUserLocale na entrada — fechou junto
> com esta data. PLANO INTEGRALMENTE ENTREGUE.
- Ativar `EasyLocalization` (hoje declarado e inerte): `ensureInitialized()` no
  `main.dart` + delegates/locales no `app_widget.dart`. Fallback en-US,
  pt-BR primeira tradução (regra já escrita no ADR do app).
- Popular `assets/translations/en-US.json` e `pt-BR.json` com a estrutura de
  chaves do setes: `app`, `auth`, `menu.groups/interfaces/privileges`,
  `register`, `forms.<entidade>.<campo>`, `feedback`, `core.errors`.
- Extrair as ~21 strings hardcoded das 7 páginas existentes do admin.
- Helper `trCatalog` (porta de `catalog_i18n.dart`): interface/módulo/privilégio
  exibem `i18n_key` traduzida com fallback para a description do banco.
- Locale por usuário: seletor de idioma (porta de `language_selector.dart` +
  `locale_sync.dart`) persistindo via `PUT /api/core/preferences`.
- Erros da API: manter mensagens por **código estável** (`error-codes.ts` já
  existe); o app traduz o código, a API não traduz (decisão da Fase 0).
- Regra operacional: chave nova sempre nos DOIS JSONs na mesma edição;
  easy_localization exige restart completo (não recarrega em hot reload).

---

## 4. Mapa de reuso

| Peça | Origem (Gestao2027) | Destino (VGR) | Ação |
|---|---|---|---|
| Auth API (login/recovery/change) | `setes-api/src/modules/auth/` | `api/src/modules/auth/` | Portar; trocar MD5→bcrypt, remover institutions |
| Mailer | `setes-api/src/shared/mailer/` | `api/src/shared/mailer/` | Portar direto |
| Guards/middlewares | `setes-api/src/gateway/` | `api/src/gateway/` | Inspirar; `requirePrivilege` é novo |
| CRUD privileges/interfaces/users | `setes-api/src/modules/{privileges,interfaces,users}/` | idem | Portar removendo institution/escopo |
| getMenus | `setes-api/src/modules/core/` | `api/src/modules/core/` | Portar simplificado (1 caminho só) |
| Auth Flutter (pages/bloc/guard/prefs) | `setes-app/packages/core/lib/src/auth/` + `shared/storage/` | `app/packages/core/lib/src/auth/` | Portar; ajustar rotas/i18n keys |
| Menu Flutter (entity→usecase) | `setes-app/packages/core/lib/src/menu/` | `app/packages/core/lib/src/menu/` | Portar; cabear `can()` |
| Preferences/locale | `setes-app/packages/core/lib/src/preference/` | `app/packages/core/lib/src/preference/` | Portar |
| Fábrica de cadastros | `setes-app/apps/web/lib/app/shared/register/` | `app/apps/admin/lib/app/shared/register/` | Portar (avaliação na Fase 4) |
| i18n (estrutura de chaves) | `setes-app/apps/web/assets/translations/` | `app/apps/admin/assets/translations/` | Usar como modelo de estrutura |

## 5. Divergências conscientes em relação ao setes

1. **Sem multi-schema / institution / contrato de interfaces** (P1, P2).
2. **Sem super nem roles mágicos** — privilégio decide tudo; bootstrap por seed (P3).
3. **Enforcement no backend por endpoint** — no setes a ACL fina é só de UI (P4).
4. **bcrypt** em vez de MD5 uppercase (VGR não tem legado Delphi a compatibilizar).
5. **CRUD de `tb_module`** — inexistente no setes; nasce no VGR (e pode voltar
   como referência para o Gestão depois).
6. **`can()` cabeado nos botões** — gancho morto no setes, ativo no VGR.
7. **"Manter logado"** — o setes decidiu não ter refresh (decisão 19 deles);
   o VGR decide o seu na Fase 0.
8. Constantes de privilégio **nomeadas** (nada de `_visualizarId = 6` mágico).

## 6. Dependências e ordem

```
Fase 0 (decisões 68+)
  └─ Fase 1 (banco + API de permissões)
       ├─ Fase 2 (auth) — independente da 3/4, pode andar em paralelo
       ├─ Fase 3 (menu dinâmico) — depende de 019 + getMenus
       │    └─ Fase 4 (telas admin) — depende da fábrica + menu
       └─ Fase 5 (i18n) — a ativação (main/app_widget) pode ser feita já;
                          as chaves crescem junto com as fases 2–4
```

Sugestão prática: ativar o EasyLocalization (Fase 5, passo 1) **antes** da Fase 2,
para que toda tela nova já nasça internacionalizada e não haja segunda passada.

## 7. Pontos em aberto — RESOLVIDOS (rodada 1 do decision-rounds)

- Enforcement backend por endpoint (`requirePrivilege`) → **decisão 72** (sim).
- Política de sessão: TTL 24h + "Manter conectado", sem refresh no MVP →
  **decisão 73**.
- `tb_admin_account` → renomear/evoluir para `tb_user` → **decisão 74**.
- Contas de equipe: criação direta pelo Admin, sem convite no MVP →
  **decisão 75**.
- Assunções a confirmar (pendências 1–2 da rodada): erros de API em inglês
  com código estável (app traduz); `kind` só 'T' no MVP.
- Item de execução (não é decisão): base URL da API hardcoded no admin
  (`app_module.dart:21`) — tornar configurável por ambiente durante a Fase 2.
