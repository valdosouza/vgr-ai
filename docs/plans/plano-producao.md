# Plano — Prontidão para produção (rodada 22)

> **Rodada 22 — ABERTA em 2026-10-10.** Valdo escolheu esta frente ("vamos
> de 2"). As pendências estão no §5; nada é construído antes das respostas e
> do "pode seguir" de cada fase (38).

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
