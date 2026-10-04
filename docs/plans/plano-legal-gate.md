# Plano — Legal Gate (bloqueio de execução por jurisdição)

> Tornar executável, auditável e reversível a decisão de **o que o VGR pode fazer em
> cada país** — substituindo o parecer de advogado como pré-requisito do
> desenvolvimento por uma análise de IA que declara o estado legal de cada
> capacidade, com o desconhecido bloqueando em produção e nunca bloqueando
> desenvolvimento nem demonstração.
>
> Data: 2026-08-03 · Status: **L0+L1 IMPLEMENTADAS** em 2026-08-03 (decisões
> 76–79 e 103–109; migração 022; 26 suítes / 151 testes verdes). Revisa a
> decisão 24. Feature doc: `api\docs\feature\legal-gate.md`.
> **L3 (telas admin) EXECUTADA em 2026-08-19** (commit 00e41be do app):
> Jurisdições (kill switch 107 com pendência de afrouxamento e confirm
> por guardas em camadas), Capacidades (veredito por jurisdição,
> `unreviewed` rotulado como bloqueio), Regras (propor com motivo
> tipificado condicional 78, histórico versionado filtrável,
> aprovar/rejeitar com recusas do servidor verbatim); a tela de
> Avaliações fica com a L2. Doc: `app\docs\feature\legal-policy.md`.
> Resta a L2 (pipeline de avaliação por IA — depende de escolher o
> provedor); a L4 foi removida pela decisão 105.

---

## 1. O problema real

Não é "falta parecer jurídico". É que **o parecer está no caminho crítico**. Hoje o
projeto tem quatro pontos onde a frase "confirmar com advogado antes do lançamento"
aparece — decisões 25 (retenção de dados de menores), 30 (promessa de recompensa),
39 (intermediação de pagamento / Lei 12.865/2013) e 8 (regras fora do Brasil). Cada
um deles é uma dívida que hoje só tem dois estados: *esperar* ou *ignorar*.

O Legal Gate cria um terceiro estado, que é o único aceitável para um produto em
andamento: **declarado, enforçado e reversível**. A capacidade fica desligada onde
não há base declarada, ligada onde há, e ligada com marca de demonstração no
ambiente de sandbox. Nada espera advogado para o código andar; e nada vai para
produção num país sem alguém ter afirmado, com nome e data, por que pode.

## 2. O que a IA pode e não pode fazer aqui

Isto precisa estar escrito, porque o desenho inteiro depende da distinção.

**Pode**: pesquisar legislação, citar dispositivos, comparar regimes, classificar
risco, propor um status por capacidade e por país, manter isso versionado e
atualizável, e cobrir dezenas de jurisdições em horas em vez de meses.

**Não pode**: emitir parecer jurídico, ser a autoridade da decisão, nem transferir
responsabilidade da operação para si. Se o produto for questionado, o que defende a
operação não é "a IA disse que podia" — é que existia **um controle explícito, com
motivo tipificado e base legal declarada, aprovado por uma pessoa identificada, com
log imutável, e a capacidade estava desligada exatamente onde não havia base**. Isso
é diligência demonstrável. "A IA disse" não é.

**Consequência de desenho, não negociável**: a IA nunca escreve a regra ativa. Ela
escreve uma *avaliação*. Um humano com privilégio promove a avaliação a regra. As
duas coisas vivem em tabelas diferentes (§6) e o log guarda as duas.

## 3. Princípios

| # | Princípio | Consequência estrutural |
|---|---|---|
| L1 | O desconhecido bloqueia | Capacidade sem regra ativa para a jurisdição = `unreviewed`, que em produção **se comporta como bloqueada**. Fail-closed, mesmo padrão do `requirePrivilege` (decisão 72). |
| L2 | Desenvolvimento e demonstração nunca são bloqueados | Jurisdição `SANDBOX` inverte o default para `allowed` e marca toda resposta como demo. É o que permite mostrar o produto ao mercado sem afirmar conformidade. |
| L3 | A IA propõe, a pessoa ativa | `tb_legal_assessment` (proposta da IA) ≠ `tb_legal_rule` (regra ativa). A promoção é ato humano, registrado. |
| L4 | Todo bloqueio tem motivo tipificado | `no_control` \| `legislation` \| `self_preservation` (decisão 78). Bloqueio sem motivo declarado não existe no modelo — a coluna é `NOT NULL`. |
| L5 | Bloqueio é instantâneo e reversível nos dois sentidos | Kill switch por jurisdição, sem deploy, sem esperar cache. |
| L6 | Nada é bloqueado silenciosamente | `tb_legal_gate_audit` append-only: quem pediu, o quê, em que jurisdição, versão da regra, resultado. |

## 4. Jurisdição aplicável — fechado pela decisão 105

O alerta original deste plano era que a decisão 68 (instalação própria por país)
resolve **soberania de dados**, mas não **jurisdição aplicável**: os regimes
relevantes alcançam pelo titular, não pelo servidor. Uma instalação `BR` que
aceitasse denunciante sob regime europeu atrairia a regra europeia, e a
instalação sozinha não saberia disso.

**A decisão 105 fecha isso pelo outro lado.** Em vez de detectar a divergência e
escalar para a regra mais restritiva, cada instalação só atende quem **está no
seu país** — a situação divergente deixa de existir e os regimes ficam isolados,
um por instalação. A fase L4 saiu do plano por causa disso.

Precisão que veio junto e que define o mecanismo: GDPR e LGPD se acionam por o
titular **estar no território**, não por nacionalidade. O controle é de
localização, não de cidadania — e o VGR já é um produto baseado em localização
(decisão 7), então o dado que a lei usa é o que o produto já precisa ter. Como
esse controle é implementado é o item 10 da rodada 2. ⚠️ **Enquanto ele não
existir, o alerta original deste parágrafo continua valendo de fato** — a
decisão 105 isola no papel; é o controle de localização que isola na prática.

## 5. Modelo conceitual — Capability × Jurisdiction → Status

**Capability** é uma *execução que carrega risco legal*. Não é endpoint (muda com
refactor), não é tela (o mesmo risco aparece em várias), não é categoria de denúncia
(granular demais e já coberta pelo RiskTier). É o verbo do domínio.

Catálogo inicial, todo ele derivado de decisões que já existem:

| Capability | Nasce da decisão | Risco que carrega |
|---|---|---|
| `report.anonymous` | 32, 23 | Anonimato social com log forense oculto de IP |
| `report.category.<key>` | 3, 9, 40 | Denúncia em categoria sensível (usa o RiskTier já existente como entrada) |
| `reward.offer` | 1, 30 | Promessa de recompensa — instituto do **Código Civil brasileiro** (arts. 854-860); pode simplesmente não existir no país X |
| `reward.monetary` | 30 | Valor entre particulares |
| `reward.intermediation.delegated` | 39, 81 | Intermediação por PSP licenciado — liberável por país onde houver terceiro contratado |
| `reward.intermediation.own` | 81 | VGR como intermediário — nasce `blocked` por `no_control` e só sai disso com autorização do BACEN (ou equivalente) |
| `reward.monetary` | 97 | Recompensa em dinheiro — bloqueada por `no_control` onde não há adapter de PSP (decisão 96). **Depende de `reward.mediation`** |
| `reward.mediation` | 98 | Decidir se a condição foi cumprida e instruir liberação/devolução do valor retido — o ponto do trilho mais próximo de prestar serviço de pagamento |
| `minor.data_retention` | 25 | Dado de criança — LGPD art. 14, GDPR art. 8, COPPA |
| `identity.disclosure` | 6, 34 | Exposição de identidade do helper |
| `location.tracking` | 7, 22, 26 | Rastro de localização e apontamento de direção |
| `data.cross_border` | (nova) | Transferência internacional de dados |
| `panic.dispatch` | 60+ | Acionamento de terceiros em emergência |

**Status**: `allowed` · `restricted` (permitido com restrição declarada) · `blocked` ·
`unreviewed` (estado inicial de tudo).

**Motivo** (só quando não é `allowed`): `no_control` (o produto ainda não tem o
mecanismo que a lei exige) · `legislation` (a lei local proíbe) ·
`self_preservation` (o risco para a operação supera o benefício).

**Dependência entre capacidades** (decisão 98): uma capacidade pode exigir
outra liberada na mesma jurisdição — `reward.monetary` exige
`reward.mediation`, porque aceitar reserva sem poder liberá-la prenderia
dinheiro de terceiro sem saída. Mínimo necessário: validação na promoção da
regra, impedindo o estado incoerente.

**Estado de revisão**: `none` → `ai_assessed` → `counsel_confirmed`. O upgrade para
`counsel_confirmed` é uma edição de linha, não uma mudança de código — é assim que o
advogado sai do caminho crítico sem sair do processo.

## 6. Modelo de dados (migração 020)

Padrão `tb_`, soft delete, coerente com o resto da API.

```
tb_jurisdiction         code (BR, PT, SANDBOX…), operational_state
                        ('live'|'restricted'|'suspended'), is_sandbox,
                        installation_default (1 linha marcada)
tb_legal_capability     key, description, module, i18n_key
                        — o catálogo de §5, semeado por migração
tb_legal_rule           capability × jurisdiction → status, reason, legal_basis,
                        review_state, version, effective_from, expires_at,
                        decided_by (FK tb_user), decided_at, deleted
tb_legal_assessment     capability × jurisdiction, model, prompt_hash, verdict,
                        confidence, citations JSON, open_questions, created_at
                        — proposta da IA; NUNCA lida em runtime pelo gate
tb_legal_gate_audit     APPEND-ONLY: capability, jurisdiction, rule_version,
                        outcome, reason, user_ref, ip, created_at
```

`tb_legal_rule` é versionada por linha (nova versão, não `UPDATE` destrutivo) — a
pergunta "o que estava valendo no dia X?" precisa ter resposta, e é exatamente a
pergunta que se faz num litígio.

## 7. Enforcement — três camadas

Uma camada só não basta, porque nem todo caminho de execução passa por HTTP.

1. **`requireCapability(capability)`** no gateway — espelha `requirePrivilege`
   (`src/gateway/require-privilege.middleware.ts`), mesmo formato de erro, mesmo
   fail-closed no `catch`. Bloqueia a rota.
2. **`legalGate.assert(capability)`** em `shared/legal/` — chamado pelo service.
   Obrigatoriamente em `shared/`, não em módulo: vários módulos precisam e a regra
   do `ARCHITECTURE.md` proíbe módulo importar módulo. Cobre fila offline
   (decisão 28), jobs e reconciliação de apontamentos (decisão 26), que nunca
   passam pelo middleware.
3. **Estado operacional da jurisdição** — verificado no mesmo lookup. `suspended`
   derruba tudo; `restricted` derruba o que não for `allowed` explícito.

**Cache**: TTL de 60s para regras, mesmo padrão do `risk-config.service.ts`, com
invalidação imediata na escrita. **Exceção deliberada**: `operational_state` tem
TTL zero. Um kill switch que demora 60s para valer não é um kill switch.

## 8. Encaixe no que já está construído

O gate não inventa infraestrutura — a Fase 1 dos controles administrativos já
entregou tudo de que ele precisa:

- **Permissão**: novas interfaces `legal-jurisdiction`, `legal-capability`,
  `legal-rule`, `legal-assessment` no `tb_interface` existente; enforcement pelo
  `requirePrivilege` (decisões 71, 72). Sem role novo, sem superusuário (decisão 70).
- **Dual-control**: `modules/admin-access/dual-control.*` já existe e é o candidato
  natural para exigir duas pessoas na ativação de uma regra (pendência 4).
- **Menu**: as telas entram no `GET /api/core/menus` como qualquer outra.
- **Auditoria**: `tb_accountability_log` **não** é reaproveitada — ela é operacional
  e mutável em desenho; o log legal precisa ser append-only e separado.

Módulos novos: `src/modules/legal-policy/` (CRUD + promoção de avaliação) e
`src/shared/legal/legal-gate.ts` (o ponto de decisão).

## 9. Fases

| Fase | Entrega | Depende de | Custo |
|---|---|---|---|
| **L0** | `shared/legal/legal-gate.ts` + catálogo hardcoded em TS + jurisdição por env + `requireCapability` + testes. Sem banco, sem tela. | nada | ~1 sessão |
| **L1** | Migração 020 + módulo `legal-policy` + cache TTL + audit | L0 | ~1-2 sessões |
| **L2** | Pipeline de avaliação por IA → `tb_legal_assessment` + promoção humana a regra | L1 | ~2 sessões |
| **L3** | Telas admin (Jurisdição, Capacidades, Regras com diff de versão, Avaliações) | L1 + **Fase 4** dos controles administrativos (a fábrica de telas) | ~2 sessões |
| ~~L4~~ | ~~Sinal de jurisdição do titular + escalonamento~~ — **removida pela decisão 105**: a divergência de jurisdição é eliminada por construção, não detectada em runtime. O que sobra é o controle de localização (item 10 da rodada 2), que pertence ao domínio de denúncia, não ao gate. | — | — |

**L0 é o que destrava agora** e não toca em nada das Fases 2–5 em andamento: uma
constante de ambiente, um middleware e um `assert`. A partir dela a demonstração ao
mercado roda em `SANDBOX` com marca de demo, e qualquer instalação real nasce com
tudo `unreviewed` — ou seja, desligada até alguém declarar o contrário.

## 10. O que o Legal Gate NÃO resolve

Vale ser explícito, porque a expectativa errada aqui custa caro:

- **Apropriação da ideia.** Geo-bloqueio trata de *execução*, não de *propriedade*. O
  ativo relevante contra apropriação já existe e é o `VGR-plano.md`: 79 decisões
  numeradas, datadas, nunca renumeradas, com o raciocínio preservado — isso é
  registro de anterioridade. O que falta é torná-lo **verificável por terceiro**
  (histórico de repositório assinado, ou hash do documento publicado
  periodicamente). Não é escopo deste plano, mas é barato e deveria ser decidido.
- **Responsabilidade pelo conteúdo das denúncias.** Marco Civil art. 19 (remoção
  mediante ordem judicial) é frente de moderação, não de capacidade.
- **Atos formais que a lei exige de uma pessoa jurídica.** Registro no BACEN
  (decisões 39, 81) é ato, não configuração. O gate consegue manter
  `reward.intermediation.own` bloqueada até o ato existir — o que é exatamente o
  valor dele: transforma uma pendência jurídica indefinida em um bloqueio técnico
  definido, e transforma "integrar o pagamento no futuro" numa linha de regra que
  vira, não num projeto a negociar de novo.

## 11. Pendências

Oito itens objetivos na **rodada 2** de `AI\docs\decisions\VGR-plano.md`, cada um com
opção recomendada. Nada de L0 em diante deve ser codado antes que a rodada 2 feche —
regra do projeto (decisões 36, 37, 38).
