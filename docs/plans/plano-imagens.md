# Plano de imagens — VGR

> Data: 2026-08-03 · Status: **rodada 7 FECHADA — decisões 126–132**; resta
> só a escolha do provedor pago (item 1, adiada de propósito pela 126 até
> haver volume real). Nada codado.
> Escopo: evidência de denúncia. Avatar ADIADO (decisão 127); vídeo e áudio
> fora até decisão própria (decisão 132).

---

## 1. Por que imagem aqui é diferente

Imagem é, ao mesmo tempo, **o dado mais reidentificador do sistema** e o
maior volume de armazenamento. Três riscos que nenhum outro dado tem juntos:

1. **Metadados embutidos (EXIF)**: uma foto de celular carrega GPS da
   captura, data/hora, modelo e às vezes número de série do aparelho. Uma
   única foto anexada a uma denúncia "anônima" pode entregar onde o
   denunciante estava — exatamente a correlação identidade↔denúncia que é o
   ativo nº 1 do plano de segurança (decisões 40/110). O anonimato social da
   decisão 23 morre num EXIF esquecido.
2. **O conteúdo pode ser ele mesmo ilegal**: cena de abuso envolvendo
   criança pode configurar armazenamento de material ilícito pelo próprio
   VGR. Isso é assunto da frente de moderação (já declarada fora de escopo
   no plano geral) e de advogado — mas o desenho de armazenamento precisa
   nascer preparado (estado `blocked`, hash por imagem, apagamento real).
3. **Arquivo de imagem é vetor de ataque**: payloads poliglotas, bombas de
   descompressão, exploits de decoder. Aceitar upload é abrir a maior porta
   de entrada de dados não confiáveis da API.

Princípio reitor herdado da decisão 110: **minimização**. A imagem que não
foi guardada não vaza, não é intimada e não custa.

## 2. Duas classes de imagem, duas réguas

| Classe | Origem | Sensibilidade | Regras |
|---|---|---|---|
| `avatar` | cadastro do usuário (opcional) | baixa | sem EXIF, pública para quem vê o perfil, sem auditoria de leitura |
| `evidence` | anexo de denúncia (pet, criança, carro, cena de violência…) | máxima | cifrada, acesso autorizado + auditado, retenção controlada |

**Avatar está ADIADO (decisão 127)** — a classe fica especificada e
desligada por config; cadastro no MVP não tem imagem. Quando for ligada:

- A decisão 119 (regra 2) já proíbe importar a foto do perfil social —
  avatar é upload local e opcional.
- Helper com avatar é um vetor (fraco, mas real) de reidentificação; a
  decisão 6 protege contra retaliação. Avatar **nunca** aparece em contexto
  de denúncia anônima.

## 3. Arquitetura de armazenamento

**Regra 1 — o banco nunca guarda o binário.** MySQL guarda só metadados
(`tb_media`); o binário vive em **object storage**. BLOB em banco não
sobrevive a "grande magnitude": incha backup, replicação e memória do pool.

**Regra 2 — o domínio não conhece o fornecedor.** Mesmo padrão da decisão 96
(`PaymentRail`): um port `BlobStore` (`put/get/delete/exists`) com adapters:

- **MVP**: adapter **S3-compatible** — a API S3 é o padrão de fato e
  funciona igual contra MinIO self-hosted, AWS S3, Cloudflare R2, Backblaze
  B2, etc.
- **Test/dev**: adapter filesystem local (zero infra para rodar a suíte).

Nenhum conceito de S3 (bucket, region, presigned) vaza para
entidade/DTO/tabela — senão trocar de fornecedor vira reescrita.

### 3.1 Degraus de custo (decisão 126)

| Degrau | Quando | Backend | Custo |
|---|---|---|---|
| 0 | dev/test | adapter filesystem | zero |
| 1 | **MVP até rodar de verdade** | **MinIO self-hosted** (mesmo servidor da API, container ou serviço Windows) | zero — só o disco que já existe |
| 2 | produção com volume real | provedor S3-compatible pago (aberto — abaixo) | por GB |

O degrau 1 usa a **mesma API S3 do degrau 2**: o adapter que vai à produção
é exercitado desde o primeiro dia, e migrar é copiar objetos (`mc mirror` /
`rclone`) e trocar env — a chave de objeto e a `tb_media` não mudam.

### 3.2 Candidatos ao degrau 2 (preços de referência de 2025/2026 — conferir na contratação)

| Provedor | Armazenamento | Egress (saída) | Brasil | Observações |
|---|---|---|---|---|
| **Cloudflare R2** | ~US$ 0,015/GB·mês (10 GB grátis) | **zero** | sem região BR dedicada | egress zero pesa muito: toda visualização de imagem sai do storage para a API |
| **Backblaze B2** | ~US$ 0,006/GB·mês | grátis até 3× o armazenado | não (US/EU) | o mais barato em repouso |
| **AWS S3 São Paulo** | ~US$ 0,04/GB·mês | ~US$ 0,15/GB | **sim (sa-east-1)** | byte dorme no Brasil; o mais caro |
| **Magalu Cloud / provedor nacional** | verificar | verificar | **sim** | soberania + pagamento em R$; maturidade a validar |
| **Wasabi** | ~US$ 7/TB·mês | zero | não | ⚠️ cobra retenção mínima de 90 dias por objeto — conflita com crypto-shredding/expiração (decisão 131) |

Leitura dos critérios: como toda visualização passa pela API (imagem
cifrada, §5), **egress importa tanto quanto repouso** — favorece R2/B2. A
jurisdição favoreceria S3 São Paulo/nacional, **mas** `evidence` é
ciphertext com chave que nunca sai da API: o provedor guarda ruído, o que
reduz o peso do critério jurisdicional (nota registrada na decisão 126).
Wasabi está de fato eliminado pela taxa de retenção mínima.

**Regra 3 — chave de objeto é aleatória e muda.** UUID v4 com sharding por
prefixo (`ab/cd/<uuid>`); a chave **nunca** contém id de usuário, de report
ou data. Enumerar o storage não pode revelar estrutura.

**Regra 4 — quem indexa é o MySQL.** `tb_media` é a única fonte de verdade:
dono, report (quando houver), classe, mime, tamanho, dimensões, hash do
original, hash do normalizado, chave de storage, DEK embrulhada, estado
(`pending → available → blocked → deleted`), timestamps de retenção. Nada de
varrer storage; busca por conteúdo (visão computacional/embeddings) é visão
futura, padrão das decisões 11/12/43/125.

## 4. Pipeline de ingestão (o coração do desenho)

Upload sempre **através da API** (nunca direto ao storage via presigned URL
— o presigned pularia exatamente as etapas que protegem o ativo nº 1):

1. **Aceitação**: multipart, allowlist de mime real por magic bytes
   (jpeg/png/webp/heic), limite de tamanho e de quantidade por denúncia
   (números na pendência 4), rate limit próprio.
2. **Hash do original**: SHA-256 registrado antes de qualquer transformação
   — integridade/cadeia de custódia se a autoridade pedir ("a imagem que
   recebemos era esta"). **O destino do original é escolha do denunciante,
   por foto (decisão 130)**: default é descartar após o passo 3; se ele
   marcar "manter dados probatórios" (com aviso do que EXIF revela, versão
   do texto registrada — padrão da decisão 86), o original é preservado
   **cifrado** como evidência ao lado do normalizado. O original nunca
   circula no app/feed — só via painel com privilégio e leitura auditada.
   Em denúncia anônima o aviso é reforçado (conflito declarado com a
   decisão 32).
3. **Re-encode obrigatório** (ex.: `sharp`): decodificar e regerar a imagem.
   Um passo, três defesas — remove **todo** EXIF/GPS/serial (anonimato),
   neutraliza payload malicioso embutido (o que não é pixel não sobrevive),
   e normaliza formato/qualidade (custo de storage previsível). O app
   Flutter também comprime e remove EXIF no cliente (defesa em profundidade
   e economia de dados móveis), mas **o servidor é a autoridade** — nunca
   confiar que o cliente limpou.
4. **Derivados**: thumbnail (feed) e tamanho de tela, gerados no ingest —
   nunca on-the-fly a partir do storage cifrado. Em categoria crítica
   (decisão 40), o derivado de feed é o **borrado** (decisão 128): o
   thumbnail nítido nunca chega ao cliente para ser "desborrado" — revelar
   é outro GET autorizado.
5. **Cifra envelope por objeto** (classe `evidence`): AES-256-GCM com DEK
   por imagem, DEK embrulhada por `MEDIA_KEK` (env, fora do banco — mesma
   mecânica da decisão 111, chave **separada** da `LEGAL_KEK`). O storage só
   vê ciphertext: bucket vazado = nada vazado. `avatar` pode ficar em claro
   (é público por definição).
6. **Registro**: linha em `tb_media` com estado `available`; evento na
   timeline do report (decisão 19) quando for anexo.

## 5. Acesso e entrega

- **Nunca público, nunca adivinhável.** Não existe URL direta de storage
  para `evidence`; a rota é `GET /api/.../media/:id` com autorização
  (visibilidade do report para o app; `requirePrivilege` no painel) e o
  servidor decifra e faz stream. Presigned URL não convive com cifra de
  aplicação — e CDN não se aplica a evidência.
- **Leitura de evidência pelo painel é auditada** (padrão
  `tb_admin_audit`/decisão 116): quem viu qual imagem de qual caso, quando.
  Admin coagido é ameaça declarada no plano de segurança.
- `avatar` pode ter cache/entrega relaxada (é a exceção, não a regra).

## 6. "A denúncia nunca espera" (decisão 123) aplicada a upload

A denúncia é registrada **sem esperar imagem nenhuma**: texto/categoria/
localização primeiro, anexos sobem **depois, em background**, pela fila
offline que a decisão 28 já obriga. No cenário "apito na praia", o pai
denuncia em segundos no 4G ruim do shopping; as fotos da criança chegam
quando a rede deixar, e entram na timeline ao chegar. Upload travando
denúncia é bug de produto, não só de rede.

## 7. Retenção e apagamento real

- **Apagar = crypto-shredding**: destruir a DEK + delete no storage. Sem a
  DEK a imagem é irrecuperável **inclusive em backup** — é o único jeito
  honesto de cumprir a decisão 25 (dados de menores: exclusão automática 90
  dias pós-resolução) e o art. 18 da LGPD num mundo com backups.
- Job de expiração no scheduler da decisão 90 (`node-cron` in-process).
- **Régua geral (decisão 131)**: 90 dias após a resolução para toda
  evidência (mesma janela da decisão 25); caso escalado a autoridade
  **congela** (mecanismo de dado congelado do Legal Gate, item 6 da
  rodada 2) até o desfecho.

## 8. O que este plano deixa pronto sem construir

- **Moderação/conteúdo ilegal** (frente separada): o hash por imagem
  (passo 2) permite hash-matching futuro; o estado `blocked` em `tb_media`
  permite bloquear sem apagar (preservação para autoridade); blur-por-default
  no feed é a pendência 3.
- **Legal Gate**: anexar mídia pode nascer como capacidade
  (`report.media`) se a rodada julgar necessário — o mecanismo das decisões
  103-109 já existe.
- **Vídeo**: mesmo port, pipeline diferente (transcoding) — fora até decisão
  própria (pendência 7).

## 9. Fases de execução

- **M1 — fundação — EXECUTADA em 2026-08-03** (liberação "pode seguir"):
  migração 028 (`tb_media`), `shared/storage` (port `BlobStore` + adapter
  filesystem + adapter S3-compatible com SigV4 próprio, testado contra o
  vetor da documentação AWS), `shared/crypto/media-cipher.ts` (DEK por
  imagem, `MEDIA_KEK` separada), módulo `modules/media` montado em
  **/app-media** (upload anônimo permitido; leitura só do dono; 404 para
  tudo que não deve servir), avatar desligado por `AVATAR_ENABLED`
  (decisão 127). 41 suítes / 253 testes. Doc:
  `api/docs/feature/media.md`. Nota de emenda: HEIC é convertido para JPEG
  **no app na captura** (sharp pré-compilado não decodifica HEIF —
  licenciamento de patente); o servidor aceita jpeg/png/webp.
- **M2 — integração com denúncia**: quando o módulo report nascer, anexo é
  aditivo (o report referencia `tb_media`, não o contrário) + evento de
  timeline + upload em background no app (fila da decisão 28) + carimbar
  `expires_at` na resolução (90 dias, decisão 131) + limite
  MEDIA_MAX_PER_REPORT (decisão 129).
- **M3 — retenção e painel — EXECUTADA em 2026-08-03** (mesma liberação):
  `gateway/scheduler.ts` (**primeiro trabalho agendado da API** — executa o
  mecanismo da decisão 90: node-cron, nunca em teste, só após migrações,
  instância única via GET_LOCK em conexão dedicada); job horário de
  expiração com **shred primeiro** (DEK zerada = fronteira de segurança) e
  delete de objetos como higiene; migração 029 com DOIS recursos kind 'R'
  (mecanismo da 93): `media_evidence` (derivados, bootstrap para admins de
  fato) e `media_original` (o original com EXIF — **sem bootstrap: ninguém
  vê até concessão humana explícita**, minimização da 110);
  `GET /api/media/...` com guardas empilhados e **toda leitura servida
  auditada** (ação `read` na tb_admin_audit, decisão 116 estendida a
  leitura; `no-store` no painel — view cacheada seria view não auditada).
  45 suítes / 267 testes.

Ordem deliberada: M1/M3 não dependem do módulo report existir — nascem como
`shared`/módulo próprio, igual o Legal Gate nasceu antes dos consumidores.
