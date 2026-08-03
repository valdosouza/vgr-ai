---
name: encapsular-widget
description: Use ao criar tela, página ou qualquer código de apresentação Flutter no VGR — garante que nenhum widget do Flutter seja usado direto, sempre via widget encapsulado Vgr* do packages/vgr_widgets (decisão 133). Também para adicionar um widget novo ao catálogo.
---

# Encapsular widget (decisão 133)

Equivalente à regra do setes-app (prefixo `Setes`), com o prefixo desta casa.

## A regra

**Nenhum widget do Flutter — ou de package externo — é usado diretamente
numa tela.** Todo widget é encapsulado em `packages/vgr_widgets` com
prefixo `Vgr`, e só ele é usado no sistema.

Motivo: trocar widget obsoleto/sem manutenção sem impactar o sistema
inteiro.

## Antes de escrever a tela

1. Abra `packages/vgr_widgets/lib/vgr_widgets.dart` e veja o catálogo.
2. Se o que você precisa existe, use.
3. Se **não** existe, adicione ao catálogo primeiro — nunca use o widget
   cru "só desta vez".

## Ao adicionar um widget ao catálogo

- Arquivo em `packages/vgr_widgets/lib/src/`, exportado no
  `vgr_widgets.dart`.
- **Exponha intenção, não interno do Flutter**: papel semântico
  (`VgrText.title`), nome de ícone por significado (`VgrIconName.delete`),
  estado (`busy: true`) — nunca `TextStyle`, `IconData` ou `EdgeInsets`
  soltos.
- Cor e tipografia saem do `Theme`, nunca de literal.
- `tooltip` obrigatório em botão só-ícone (leitor de tela).
- Cubra com teste em `packages/vgr_widgets/test/`.
- Acrescente o widget cru correspondente à lista da guarda em
  `apps/admin/test/design_system_guard_test.dart`.

## Convenções que o catálogo já fixou

| Em vez de | Use |
|---|---|
| `Text('x')` | `VgrText('x')`, `VgrText.title(...)`, `VgrText.error(...)` |
| `SizedBox(height: 16)` | `VgrGap.md()` |
| `Scaffold` + `AppBar` | `VgrScaffold(title:, body:)` |
| `ElevatedButton` + spinner manual | `VgrPrimaryButton(busy:)` |
| `Icon(Icons.delete_outline)` | `VgrIcon(VgrIconName.delete)` |
| `showDialog` + `AlertDialog` | `showVgrConfirm` / `showVgrDialog` / `showVgrTextPrompt` |
| `ScaffoldMessenger...SnackBar` | `showVgrMessage(context, msg)` |
| `StatefulBuilder` em diálogo | `VgrStatefulContent` |

## Nos testes

Afirme sobre o widget da casa, nunca sobre o interno:

```dart
tester.widget<VgrIconButton>(find.byKey(const Key('approve-1')));  // ✔
tester.widget<IconButton>(find.byKey(const Key('approve-1')));     // ❌
```

## Verificação

`cd apps/admin && flutter test test/design_system_guard_test.dart`

A guarda lista arquivo e linha de cada violação. Ela existe porque a regra
ficou escrita e ignorada em ~350 lugares até ser verificada por teste.

## Referências

- `app/docs/adr/DESIGN-SYSTEM.md` — o padrão completo
- `AI/docs/decisions/VGR-plano.md` — decisão 133
- Origem: `D:\Gestao2027\Infra-IA\setes-app\prompt_fase1_fundacao.md` §B
