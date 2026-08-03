# Autenticação dos usuários do app (denunciante e helper)

> Data: 2026-08-03 · Status: **rodada 5 FECHADA — decisões 119–125**.
> Cinco métodos (120); vínculo verificado dos dois lados (121); access
> 30min + refresh rotativo 90d (122); "a denúncia nunca espera" (123);
> senha min 12 / TOTP opcional, sem colisão com social (124); visão de
> helpers profissionais (125). Nada codado — implementação atrás/junto das
> fases S1–S6 (decisão 38).
> Relação: decisões 4, 23, 31-35, 60, 110-118; tasks 13/17 do
> `003-api-tactical-design.md` (UserAccount / AuthenticateWithProvider).

---

## 1. O que já estava decidido (e continua valendo)

- **Decisão 31**: login social = Google, Apple, Facebook + **OTP por
  telefone/WhatsApp** como 4º método. A mensagem de 2026-08-03 do dono do
  produto **acrescenta e-mail/senha** — item 1 da rodada 5 confirma o
  conjunto final.
- **Decisões 32/35**: denunciante anônimo e helper anônimo **não se
  autenticam** — fluxo sem conta e sem token continua existindo e é
  intocável por este plano. Autenticação só é exigida quando a ação exige
  identidade (oferecer recompensa — 33; reivindicar recompensa — 34).
- **Decisão 60**: identidade vive no plano administrativo. O app opera
  anônimo socialmente; a plataforma conhece quem se registrou.
- **Tasks 13/17** já especificam `UserAccount` (consentimento obrigatório,
  jurisdição BR fixa) e `AuthenticateWithProvider` (verificação server-side
  do token do provedor, upsert idempotente).

## 2. Diretriz — decisão 119: dois planos de autenticação, nunca cruzados

| | Painel (tb_user) | App (UserAccount) |
|---|---|---|
| Quem | equipe/admins | denunciante, helper |
| Métodos | e-mail+senha, 2FA TOTP obrigatório (114) | social (31) + e-mail/senha (119) + OTP |
| Sessão | 15 min, session_version (112) | item 3 da rodada 5 |
| JWT | `aud: "admin"` | `aud: "app"` |
| Tabelas | tb_user (+privilégios) | tb_user_account (+provedores) |

Regras fixadas pela 119 (detalhe na decisão): audiences distintos e
rejeição cruzada nos middlewares; token de provedor social verificado
server-side (assinatura, iss, aud, exp, nonce) e **nunca armazenado**;
minimização no que vem do provedor (sub, e-mail, flag de e-mail
verificado, nome de exibição — nada de foto, grafo, telefone do perfil);
uma conta N provedores via tabela de vínculo; senha (quando houver) com
bcrypt, mesmas regras de log da 110.

## 3. Rodada 5 — em `VGR-plano.md`

1. OTP telefone/WhatsApp continua no conjunto? (31 dizia sim; a mensagem
   nova não o citou)
2. Vínculo de contas com o mesmo e-mail entre provedores (vetor clássico de
   account takeover)
3. Sessão do app: TTL e renovação
4. Verificação de e-mail no cadastro por senha
5. Política de senha e 2FA do usuário do app

## 4. Segurança herdada que já cobre este plano

Rate limit em /auth (10/min) + atraso progressivo por conta (113) valerão
para o login do app; fail-fast de env (110/A2); erros `{error, code}` sem
enumeração de conta (padrão do recovery admin); auditoria de auth do app
entra na tb_admin_audit? **Não** — ações de usuário final não são CRUD
administrativo; o rastro relevante é o accountability log (23) e o log de
sessão que o item 3 definir.
