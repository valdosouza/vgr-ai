# Plano de segurança de software — VGR

> Data: 2026-08-03 · Status: **rodada 4 FECHADA — decisões 110–118**; A1–A3
> corrigidos; execução por fases em §8, aguardando liberação fase a fase
> (decisão 38).
> Escopo: software (API + app). Segurança física e de servidor é assunto de
> implantação — §6 traz apenas as instruções que a implantação deve seguir.

---

## 1. Por que a segurança aqui é diferente

Num e-commerce, o pior incidente é vazamento de cartão. **Aqui, o pior
incidente é a correlação entre uma denúncia e a identidade de quem a fez ou de
quem ajudou** — nas categorias da decisão 40, isso é risco de morte por
retaliação de crime organizado. Dinheiro é recuperável; deanonimização não.

Disso segue a hierarquia de ativos (o que se protege primeiro):

| # | Ativo | Onde vive | Decisões |
|---|---|---|---|
| 1 | **Correlação identidade ↔ denúncia/ajuda** | `tb_accountability_log` (IP, metadata), futuros Report/HelpOffer, timeline | 6, 23, 32, 40, 44, 55, 60 |
| 2 | Identidade dos usuários registrados | `tb_user`, futuro UserAccount | 4, 34 |
| 3 | Localização (posição, trilhas, avistamentos) | futuros Report/sightings | 7, 22, 26 |
| 4 | Integridade das decisões administrativas | privilégios, dual-control, Legal Gate, regras de risco | 45, 70-75, 107 |
| 5 | Instruções de pagamento (nunca o dinheiro — custódia zero) | futuro PaymentIntent | 84, 100 |

O modelo de ameaça correspondente, em uma linha cada:

- **Criminoso organizado** tentando descobrir quem denunciou/ajudou — via
  invasão do banco, via correlação temporal (decisão 41 já mitiga), via
  extrato de pagamento (decisões 58/82 já mitigam), ou via um admin coagido.
- **Admin malicioso ou coagido** — mitigado por duplo controle (45/107) e
  por privilégio por endpoint (72); resta auditar o que ele faz (item 6).
- **Atacante externo comum** — credential stuffing, brute force, injeção,
  XSS no painel web.
- **O próprio Estado/"sistema"** (contexto declarado do projeto) — mitigado
  pelo Legal Gate (bloqueio declarado, não improviso) e por minimização: o
  que não foi coletado não pode ser intimado.

**Princípio reitor (decisão 110): minimização.** A defesa mais barata e mais
forte deste produto é não ter o dado. Todo campo novo que identifique alguém
precisa justificar por que existe, quanto tempo vive e quem o lê.

## 2. O que já existe (inventário verificado em 2026-08-03)

Camadas já construídas e testadas, com o arquivo que as prova:

- **AuthN**: JWT Bearer em todo `/api` (`gateway/auth.middleware.ts`); bcrypt
  para senhas (login e recovery); recovery com código de 6 dígitos, TTL 15
  min, resposta silenciosa para e-mail inexistente e 401 genérico.
- **AuthZ**: `requirePrivilege` por endpoint, default-deny, fail-closed
  (decisão 72); duplo controle para dado criptografável (45) e para o Legal
  Gate (107); sem superusuário (70).
- **Legal Gate**: fail-closed por capacidade e jurisdição, kill switch,
  auditoria append-only (103-109).
- **Entrada**: Zod em todo body (`parseBody`), SQL 100% parametrizado
  (`pool.query` com `?` em todos os repositórios — verificado), limite de
  payload 2 MB.
- **Rate limit**: 100/min geral, 10/min em `/auth` (brute-force alvo).
- **Erros**: envelope `{ error, code }` sem stack trace nem SQL vazando
  (decisões 80/83); `handleError` central.
- **Anonimato por desenho**: log de responsabilização append-only sem rota
  de leitura pública (23); sinais de engajamento ocultos em categoria
  crítica (41); identidade só no plano administrativo (60/82).
- **App**: token só em memória a menos que "manter conectado" (decisão 73);
  senha nunca persistida; decode de JWT client-side é advisory (API é a
  autoridade).

## 3. Achados da auditoria

### Corrigidos nesta sessão (objetivos, sem decisão de produto)

| # | Achado | Gravidade | Correção |
|---|---|---|---|
| A1 | **Logger de debug registrava o body de toda requisição** — incluindo `{ email, password }` de cada login, em texto claro no log. Estava marcado "TEMP — remove after manual QA". | **Crítica** | Removido de `app.ts`. Regra registrada na decisão 110: log nunca recebe segredo, senha, token ou body bruto; se precisar de log de request em dev, é allowlist de campos. |
| A2 | **`JWT_SECRET ?? ''`** no verify e no sign — com env ausente, qualquer um forja token válido com segredo vazio. | **Crítica** | `shared/config/env.ts` (`jwtSecret()` lança se ausente); middleware responde 500 em vez de aceitar; `server.ts` recusa boot em produção sem o segredo. |
| A3 | **Swagger público em produção** — `/docs` e `/docs.json` expõem a superfície inteira da API. | Média | Gate: fora de produção sempre; em produção só com `SWAGGER_ENABLED=true`. |

### Abertos — viram a rodada 4 (item entre parênteses)

| # | Achado | Gravidade | Situação |
|---|---|---|---|
| B1 | **Decisão 44 (criptografia em repouso) decidida e NÃO implementada** — `tb_accountability_log.ip_address` está em texto claro, e é exatamente o ativo nº 1. | **Alta** | Item 1 da rodada 4 — o *como* (envelope, chave, escopo). |
| B2 | **Token de 24h sem revogação** — usuário desativado/demitido mantém acesso até expirar; papel vem do token, não do banco. | Alta | Item 2. |
| B3 | **Sem lockout por conta** — rate limit é só por IP; código de recovery tem espaço de 10⁶ e nenhum contador de tentativas por conta. | Alta | Item 3. |
| B4 | **Senha mínima de 5 caracteres** (`user.dto.ts`). | Média | Item 4. |
| B5 | **Sem headers de segurança nem CORS estrito** — `CORS_ORIGIN=*` default, sem HSTS/CSP/nosniff, sem `trust proxy` (rate limit por IP confiando em X-Forwarded-For). | Média | Item 5. |
| B6 | **Ações administrativas sem auditoria geral** — Legal Gate e dual-control auditam; CRUD de usuário/privilégio/regra de risco não registra quem fez o quê. | Média | Item 6. |
| B7 | **Token no painel web em localStorage** — acessível a XSS (mobile tem opção melhor: secure storage). | Média | Item 7. |
| B8 | **Sem verificação de dependências** — nenhum `npm audit`/lockfile check automatizado (não há CI ainda). | Baixa | Item 8. |

## 4. O modelo — seis camadas

O que a rodada 4 completa, somado ao que existe, forma este modelo (cada
camada falha fechada e independente das outras):

```
SEC-1  Minimização        não coletar / não reter / não logar (110)
SEC-2  Borda              headers, CORS estrito, rate limit, lockout, validação Zod
SEC-3  Identidade         senha forte, sessão curta revogável, secure storage
SEC-4  Autorização        requirePrivilege + dual-control + Legal Gate  ✅ construída
SEC-5  Dado em repouso    envelope encryption no ativo nº 1, chave fora do banco (44)
SEC-6  Rastreabilidade    auditoria append-only de toda ação administrativa
```

## 5. Regras permanentes de desenvolvimento (decisão 110)

Valem para todo código novo, entram no code review como bloqueantes:

1. **Log nunca recebe** senha, token, código de recuperação, body bruto,
   IP de denunciante fora do log de responsabilização, ou localização.
2. **SQL sempre parametrizado** — string interpolada em query é defeito,
   mesmo em migração ou script.
3. **Todo endpoint novo nasce com** `requirePrivilege` (ou justificativa
   explícita de rota pública) — e, se tiver risco legal, `requireCapability`.
4. **Erro para fora é `{ error, code }`** — detalhe fica no logger.
5. **Campo identificável novo** exige: por quê, TTL, quem lê — no PR.
6. **Segredo só em env** — nunca em código, migração, teste ou fixture.

## 6. Instruções para a implantação (fora do escopo de software)

Registradas aqui para o dia da infra; nada disso é código:

- TLS obrigatório ponta a ponta; HSTS; certificado gerenciado.
- Banco inacessível da internet; usuário da API sem DDL além do runner de
  migração; backup criptografado com chave separada do backup.
- `JWT_SECRET` e futura KEK da decisão 44 em secret manager (nunca em
  arquivo no repositório); rotação documentada.
- `CORS_ORIGIN` com a origem real do painel; `SWAGGER_ENABLED` ausente.
- Log de aplicação com retenção curta e acesso restrito (ele é, por
  construção, pobre em dados — SEC-1).
- Uma instalação por país (decisão 68) também é fronteira de segurança:
  comprometimento de uma não expõe as outras.

## 8. Execução — fases para liberação (decisão 38)

Ordenadas por dano-evitado ÷ esforço. Cada fase termina com `tsc` limpo e
suíte verde; nenhuma depende da seguinte.

| Fase | Conteúdo | Decisões | Esforço |
|---|---|---|---|
| **S1 — borda e política** | helmet + CORS estrito com fail-fast + trust proxy; senha min 12 + lista de proibidas nos DTOs; `engines` no package.json; checklist de release com `npm audit` | 115, 114(senha), 118 | ~1 sessão |
| **S2 — sessão revogável** | migração 023 (`session_version`, contadores de falha); TTL 15m; verificação de versão no authMiddleware via cache do privilege-store; atraso progressivo no login; código de recovery invalidado na 5ª falha; app renovando silenciosamente | 112, 113 | 1-2 sessões |
| **S3 — criptografia em repouso** | `shared/crypto/envelope.ts` (AES-256-GCM, DEK por registro, `LEGAL_KEK` com fail-fast); migração 024 (colunas cifradas no accountability log); escrita cifrada; decifra SÓ pelo fluxo dual-control | 111, 44, 45 | 1-2 sessões |
| **S4 — auditoria administrativa** | migração 025 (`tb_admin_audit`); helper fire-and-forget em `shared/`; chamadas nos 6 services de CRUD | 116 | ~1 sessão |
| **S5 — 2FA TOTP** | tabela de segredo + códigos de recuperação; enrolamento obrigatório no 1º login; verificação no login; destrave por dual-control; telas no app | 114(2FA) | fase própria, 2-3 sessões |
| **S6 — app** | `flutter_secure_storage` no mobile; tela do 451 com motivo tipificado | 117 | ~1 sessão |

## 7. Referências

- Decisões 110 e rodada 4: `AI\docs\decisions\VGR-plano.md`.
- Legal Gate (SEC-4): `plano-legal-gate.md`, `api\docs\feature\legal-gate.md`.
- Controles administrativos (SEC-4): `plano-controles-administrativos.md`.
- Criptografia e duplo controle (SEC-5): decisões 44/45.
