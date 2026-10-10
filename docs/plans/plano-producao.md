# Plano — Prontidão para produção (rodada 22)

> **Rodada 22 — aberta e respondida em 2026-10-10** ("1a, 2a, 3a, 5a, 6a,
> 7a, 8a, 9a, 10 ok"). Decisões **240–248** no
> [VGR-plano.md](../decisions/VGR-plano.md). Em aberto só o item 4
> (domínio), necessário antes da P3. Cada fase por "pode seguir" (38) — §6.
> **Decisão 249** (2026-10-10, durante a P2): Garage no lugar do MinIO,
> que deixou de publicar imagens. **Item 11 em aberto** (§5): a
> jurisdição da homologação com convidados.

---

## 1. Origem

Todas as frentes do MVP têm software entregue e testado em navegador
(VGR-RESUMO §4 e §6, 5h/5i). Faltava responder: **dá para colocar isto no
ar?** O levantamento de 2026-10-10 leu os três repositórios e testou o
caminho de produção da API. A resposta curta: a segurança da aplicação está
pronta, o caminho de implantação não existe.

## 2. O que já está pronto

- **Segurança da aplicação** (plano-seguranca.md, rodada 4): helmet, CORS
  estrito, `trust proxy`, sessão revogável, 2FA, criptografia envelope do
  accountability log e das imagens, auditoria administrativa.
- **Recusa de boot em produção** (`NODE_ENV=production`) sem `JWT_SECRET`,
  sem lista explícita de `CORS_ORIGIN`, sem `LEGAL_KEK` ou `MEDIA_KEK`, ou com
  S3 incompleto.
- **Decisões de infraestrutura já tomadas**: MariaDB (231); MinIO no mesmo
  servidor da API no MVP, provedor S3 pago depois (126); uma instalação por
  país (68); instruções de implantação do plano de segurança §6 (TLS, banco
  fechado para a internet, backup cifrado, logs com retenção curta).
- **CI** nos dois repositórios de código (typecheck e testes na API;
  analyze e testes no app).
- `GET /health` responde 200.

## 3. Bloqueios encontrados (verificados em 2026-10-10)

| # | Bloqueio | Como foi verificado |
|---|---|---|
| B1 | **A API compilada não sobe.** `npm run build` + `npm start` (o comando de produção do `package.json`) quebra com `Cannot find module '@gateway/auth.middleware'`: o `tsc` não reescreve os atalhos `@gateway/`, `@modules/`, `@shared/`. | executado |
| B2 | **As migrações não vão para o build.** Os `.sql` ficam em `src/migrations/sql` e o `tsc` não os copia. O runner, sem a pasta, não acha nada e loga "Migrations completed": corrigido o B1, a API subiria **sem criar o banco** e sem avisar. | `dist/` com 0 arquivos `.sql`; leitura do `runner.ts` |
| B3 | `db:migrate` e `seed:admin` rodam com `tsx`, que é dependência de desenvolvimento: num servidor instalado só com as dependências de produção, não existem. | `package.json` |
| B4 | **O painel aponta fixo para `http://localhost:3002`** (TODO no código esperando esta decisão). | `apps/admin/lib/app/app_module.dart` |
| B5 | O app mobile lê a URL da API de `--dart-define=API_URL` (padrão localhost), o que está certo; mas o client id do login Google está fixo no código (TODO). | `app_module.dart`, `auth_module.dart` |
| B6 | **O APK de release é assinado com a chave de debug.** A Play Store recusa. | `android/app/build.gradle.kts` |
| B7 | A API supõe **uma instância só**: jobs agendados dentro do processo (90), limite de requisições em memória, `trust proxy = 1` (exatamente um proxy na frente). Serve para um servidor; duas instâncias quebrariam os três. | código |
| B8 | **Apagar só é definitivo quando o backup expira.** O crypto-shredding (131, 25) apaga a chave cifrada da imagem, mas essa chave mora na linha do banco (`dek_wrapped`): um backup do banco feito antes do apagamento ainda a tem. A retenção do backup é o prazo real de apagamento. | `028_media.sql`, `media.repository.ts` |
| B9 | **Perder `LEGAL_KEK` ou `MEDIA_KEK` é perder tudo o que é cifrado** (accountability log e todas as imagens). Não há cópia de segurança das chaves prevista em lugar nenhum. | decisão 111 |

B1–B6 são correções sem decisão de produto. B7–B9 entram nas decisões
abaixo.

## 4. O que esta frente NÃO decide

Provedor de pagamento (59), provedor de SMS/OTP, IA de moderação L2 (144) e
revisão jurídica (228) continuam como estão. O item 9 só decide **o que
pode abrir enquanto elas não fecham**.

## 5. Pendências (rodada 22 — prontidão para produção)

**Respondidas em 2026-10-10**, todas na opção recomendada: 1a → 240,
2a → 241, 3a → 242, 5a → 243, 6a → 244, 7a → 245, 8a → 246, 9a → 247,
10 → 248. **Em aberto: item 4 (domínio)**, necessário antes da P3, e o
**item 11** (abaixo, surgiu na P2). O texto original das opções fica
abaixo como registro.

**1. Onde hospedar o MVP**
- (a) **Um servidor (VPS) no Brasil** com API, MariaDB, MinIO e o proxy com
  TLS, como a 126 já supõe. O provedor é escolha comercial sua. *(Recomendado:
  menor custo, condiz com 126 e 68, e o B7 deixa de ser problema.)*
- (b) Nuvem gerenciada desde o início (banco gerenciado + S3 pago).
- (c) Outro.

**2. Como empacotar**
- (a) **Docker Compose** no servidor: api, mariadb, minio e Caddy (TLS
  automático), tudo descrito no repositório. *(Recomendado: o servidor vira
  reproduzível e homologação é uma cópia.)*
- (b) Instalação direta (Node, MariaDB e MinIO como serviços do sistema).

**3. Ambientes**
- (a) **Produção + homologação** no mesmo servidor, com bancos, buckets e
  chaves separados. *(Recomendado: migração e app novos passam primeiro por
  homologação.)*
- (b) Só produção no MVP.
- (c) Homologação em outro servidor.

**4. Domínio** — informar o domínio. Endereços propostos: `api.<domínio>`,
`painel.<domínio>` e, se 3(a), `api-homolog.<domínio>` e
`painel-homolog.<domínio>`.

**5. Segredos** (`JWT_SECRET`, `LEGAL_KEK`, `MEDIA_KEK`, SMTP, MinIO)
- (a) **No servidor único: arquivo de ambiente fora do repositório,
  legível só pelo serviço; cópia das duas chaves-mestras num cofre offline
  (gerenciador de senhas), com acesso de duas pessoas.** Gerenciador de
  segredos de nuvem quando sair do servidor único. *(Recomendado. Revisa o
  "secret manager na implantação" da 111 para o MVP e fecha o B9.)*
- (b) Gerenciador de segredos (Vault ou de nuvem) desde o início.

**6. Backup** (fecha o B8)
- (a) **Dump diário do MariaDB cifrado com chave própria + espelho do
  MinIO, cópia fora do servidor, retenção de 30 dias, teste de restauração
  antes de abrir.** Um dado apagado some por completo em até 30 dias, e o
  aviso de privacidade diz isso. *(Recomendado.)*
- (b) Igual, com retenção de 7 dias (apaga mais rápido, recupera menos).
- (c) Igual, com retenção de 90 dias.

**7. Monitoramento e logs**
- (a) **Checagem externa do `/health` a cada minuto com alerta (e-mail ou
  WhatsApp) + logs com rotação de 14 dias no servidor** (retenção curta do
  plano de segurança §6). *(Recomendado.)*
- (b) Pilha completa de observabilidade (métricas, painéis, logs
  centralizados) já no MVP.

**8. Distribuição do app**
- (a) **Android primeiro** (Play Console: teste interno → produção), iOS
  depois; chave de assinatura de release fora do repositório (Play App
  Signing). Precisa da sua conta de desenvolvedor. *(Recomendado.)*
- (b) Android e iOS juntos.
- (c) Só web no começo.

**9. O que abre antes das pendências externas** (jurídico 228, PSP 59, OTP)
- (a) **Fase fechada primeiro**: homologação com convidados, recompensa em
  dinheiro desligada; abertura ao público só depois da revisão jurídica.
  *(Recomendado.)*
- (b) Abrir ao público já, sem recompensa em dinheiro.
- (c) Esperar todas as pendências externas.

Nota: verificação de e-mail e recuperação de senha precisam de um
remetente SMTP de verdade (escolha comercial, como a 59). Sem ele, cadastro
e recuperação não funcionam fora do desenvolvimento.

**10. Fatiamento** (proposta)
- **P1**: correções sem decisão (B1–B6): build de produção da API que sobe e
  aplica migrações, scripts de migração e seed sem ferramentas de
  desenvolvimento, URL da API e client id do Google por ambiente no painel e
  no app, assinatura de release por chave externa.
- **P2**: kit de implantação no repositório: Dockerfile, compose, Caddy,
  scripts de backup e restauração, roteiro de implantação (runbook).
- **P3**: subir homologação no servidor escolhido. Precisa do servidor: você
  segue o roteiro, ou me dá acesso.
- **P4**: primeira versão Android na faixa de teste interno.

Cada fase por "pode seguir" (38).

**11. Jurisdição da homologação com convidados** (surgiu na P2)

Com `LEGAL_JURISDICTION=BR`, toda funcionalidade com Legal Gate (denúncia
anônima, chat, pânico, avaliação, apontamento de direção) responde 451 até
existir uma regra ativa para ela, aprovada no painel (104, fail-closed).
Essas regras são justamente o que a revisão jurídica (228) produz. A fase
fechada da 247 roda na homologação, com pessoas reais.
- (a) **Homologação em BR, como produção**: os convidados só usam o que
  tiver regra aprovada; as primeiras regras são criadas no painel antes de
  abrir. *(Recomendado: a fase fechada testa o produto como ele vai
  funcionar, e nenhum dado de pessoa real passa por funcionalidade sem
  regra.)*
- (b) Homologação em SANDBOX (79, "onde as demos rodam"): tudo liberado
  salvo bloqueio explícito, enquanto a revisão jurídica não sai.

## 6. Fases

| Fase | Conteúdo | Depende de | Estado |
|---|---|---|---|
| **P1** | B1–B6: build de produção da API que sobe e aplica migrações; scripts de migração e seed sem ferramenta de desenvolvimento; URL da API e client id do Google por ambiente no painel e no app; assinatura de release por chave externa | — | **executada em 2026-10-10** (api `4063846` + `622e99d`, app `3cab7a3`) — §7 |
| **P2** | Dockerfile, compose (api, mariadb, Garage — 249, Caddy) para produção e homologação, backup e restauração (244), checagem de saúde e rotação de logs (245), roteiro de implantação | P1 | **executada em 2026-10-10** (api `5f39112` + `7021e3e`) — §7 |
| **P3** | homologação no servidor escolhido (240) | P2 + domínio (item 4) + item 11 + servidor + contas (armazenamento externo do backup, SMTP, monitor) | aguardando |
| **P4** | primeira versão Android no teste interno (246) | P1 + conta Play Console | aguardando |

## 7. Execução

### P1 — 2026-10-10

**API** (api `4063846` dependências, `622e99d` build):
- `npm run build` agora compila `src/` sem os testes, reescreve os atalhos
  `@gateway/`/`@modules/`/`@shared/` para caminhos relativos (`tsc-alias`)
  e copia os `.sql` para `dist/migrations/sql` (B1, B2).
- O runner **recusa subir** se não acha nenhuma migração, em vez de dizer
  "Migrations completed" sobre um banco vazio. Testado com pasta real
  vazia e ausente.
- `run-migrations` e `seed-admin` foram para `src/cli` e rodam com Node
  puro: `npm run db:migrate:prod`, `npm run seed:admin:prod` (B3).
- O CI compila e roda um teste de fumaça do `dist/` (o app carrega com Node
  puro e leva todas as migrações), e bloqueia vulnerabilidade alta ou
  crítica nas dependências de produção — o portão que o `RELEASE.md`
  (decisão 118) previa para quando houvesse CI.
- **Achado no caminho**: `npm audit` acusava 12 vulnerabilidades nas
  dependências de produção, 1 crítica e 6 altas. A crítica (`proxy-addr`)
  permite forjar o IP atrás de proxy, e o accountability log (23) guarda
  esse IP. Corrigidas todas as altas e a crítica; o `nodemailer` subiu de
  versão maior (9 → 10) e um e-mail de verdade foi enviado a um servidor
  SMTP local. Ficam 2 moderadas (`uuid` via `google-auth-library`), cuja
  correção pede versão maior dessa biblioteca.
- **Conferido de ponta a ponta** em MariaDB vazio, numa pasta só com as
  dependências de produção: migração (40 arquivos, 45 tabelas), criação do
  primeiro admin, `npm start`, `/health` 200, login do painel pedindo o
  cadastro do 2FA. Sem a pasta de migrações, a API se recusa a subir.
- Suíte 122/122, 1233 testes; `tsc` limpo.

**App** (app `3cab7a3`):
- Painel: a URL da API vem de `--dart-define=API_URL` (antes fixa em
  localhost) (B4).
- App: o client id do Google vem de `--dart-define=GOOGLE_SERVER_CLIENT_ID`
  (B5).
- Android: release assina com a chave de upload apontada por
  `android/key.properties` (fora do repositório); sem ele, o build de
  release **para** com instruções. Debug e profile não mudam (B6).
- `docs/feature/release.md`: comandos por ambiente, chave de upload, o que
  recusa.
- Conferido: os builds web dos dois apps levam os valores passados e não os
  padrões; analyze limpo; admin 392 e mobile 433 testes verdes. A regra do
  Gradle rodou no Gradle 8.14 com tarefas de teste (debug/profile passam,
  as duas de release param, ambas leem o `key.properties`). **O build
  Android completo não rodou**: o SDK do Android não pôde ser baixado neste
  ambiente (o proxy de rede bloqueia `dl.google.com`). O primeiro
  `flutter build appbundle --release` com a chave de upload confirma o
  resto (P4).

### P2 — 2026-10-10

**API** (api `5f39112` `/health`, `7021e3e` kit):
- `/health` agora consulta o banco (`SELECT 1`, limite de 2 s) e responde
  **503** quando ele não responde. Antes respondia 200 com o MariaDB fora:
  a checagem externa da 245 não veria a queda.
- **Imagem da API** (`Dockerfile`): etapa de build roda o build e o teste
  de fumaça da P1; a imagem final só tem dependências de produção, roda
  sem root e tem checagem de saúde.
- **`deploy/compose.yaml`**: Caddy (TLS automático, HSTS, arquivos do
  painel; único serviço com portas abertas), `api` (produção) e
  `api-homolog` (construída no servidor e promovida para produção depois
  de testada), MariaDB com um banco e um usuário por ambiente, Garage
  (249) com um bucket e uma chave por ambiente. Banco e Garage ficam numa
  rede interna, sem saída para a internet. Logs no journald, 14 dias.
- **Segredos** só em `/etc/vgr`, com modelos em `deploy/env` (243).
- **Backup** (244): dump de cada banco cifrado com `age` para uma chave
  pública — a chave privada fica no cofre offline, então o servidor não
  consegue ler os próprios backups; imagens espelhadas com `rclone`
  (objeto apagado vai para `removed/<dia>`); tudo copiado para fora do
  servidor; o que passa de 30 dias é apagado. `restore.sh` restaura num
  banco de teste e recusa sobrescrever um banco em uso sem
  `--into-live`. Timer diário às 03:30 de Brasília.
- **Roteiro**: `api/docs/adr/DEPLOY.md`, do servidor vazio às
  atualizações (homologação primeiro) e ao rollback.

**Conferido subindo tudo com Docker neste ambiente:**
- as duas APIs saudáveis e migradas;
- TLS pelo Caddy (HTTP/2, HSTS, HTTP redireciona para HTTPS);
- o painel aberto pelo Caddy, fazendo login até a tela obrigatória do 2FA;
- o adaptador S3 da própria API no Garage; a chave da homologação
  recusada no bucket de produção (403) e o usuário de banco da homologação
  recusado no banco de produção;
- backup; objeto apagado indo para `removed/<dia>`; pastas e dumps com
  mais de 30 dias apagados aqui e fora do servidor;
- restauração de teste igual ao banco em uso (45 tabelas, 40 migrações,
  o usuário admin);
- `/health` 503 com o MariaDB parado e 200 quando ele volta;
- `shellcheck` limpo; suíte da API 122/122, 1235 testes.

**Não conferido aqui**: os certificados públicos do Let's Encrypt (precisam
do domínio e do servidor — P3), o journald de verdade (este ambiente não
tem; o teste usou o log padrão do Docker), e o build da imagem sem o
certificado do proxy deste ambiente (o teste usou uma cópia do Dockerfile
que só acrescenta esse certificado).

