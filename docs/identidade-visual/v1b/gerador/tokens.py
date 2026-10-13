"""VGR identity tokens, consolidated direction (round 24, decisions 261-264).

Source of the colors V2 takes into vgr_widgets. Every pair in PAIRS is
checked against the WCAG AA floor of decision 257 (run: python3 -B tokens.py).
"""

def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminance(hexcolor):
    h = hexcolor.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

FONT = 'Atkinson Hyperlegible Next'
SLOGAN = 'Pessoas cuidando de pessoas. Comunidades mais seguras.'

# Roles:
#   bg / surface        page and cards
#   text / muted        main and secondary text
#   brand / onBrand     the navy of the mark: app bar marks, links, selection
#   action / onAction   the teal of Valdo's board: filled buttons, FAB
#   accent / onAccent   the gold as a fill (the reward seal of decision 101)
#   accentGraphic       the gold as a graphic on the theme's surfaces (>= 3:1)
#   accentText          the gold as text (>= 4.5:1)
#   control             checkbox and field borders (>= 3:1)
#   divider             decorative lines (no contrast floor)
#   danger / onDanger   panic and errors only (decision 253)
#   navStrong / navSoft the two navigation columns of the panel (decision 215)
#   splash              the opening screen background
TOKENS = {
    'light': dict(
        bg='#F4F6F8', surface='#FFFFFF', text='#131D33', muted='#627289',
        brand='#203B70', onBrand='#FFFFFF', action='#1B7168', onAction='#FFFFFF',
        accent='#D8A34D', onAccent='#131D33', accentGraphic='#BB8329', accentText='#946820',
        control='#788499', divider='#DDE2EA', danger='#D23535', onDanger='#FFFFFF',
        navStrong='#E6EAF1', navSoft='#F7F8FB', splash='#203B70'),
    'dark': dict(
        bg='#0A1120', surface='#111A2D', text='#E9EDF6', muted='#A9B3C9',
        brand='#93B6FF', onBrand='#0A1120', action='#5CCDBB', onAction='#05201C',
        accent='#D8A34D', onAccent='#0A1120', accentGraphic='#D8A34D', accentText='#D8A34D',
        control='#7D88A3', divider='#243049', danger='#FFB4AB', onDanger='#4A0B07',
        navStrong='#18233A', navSoft='#141E33', splash='#0A1120'),
}

# The mark itself, outside the themes: the app icon and the negative logo
# sit on the navy in both modes.
MARK = dict(navy='#203B70', white='#FFFFFF', gold='#D8A34D')

# What changed from the board (decision 261): (role, board, now, why).
BOARD_FIXES = [
    ('dourado como gráfico no claro', '#D8A34D', '#BB8329', 'sobre branco dava 2,27:1; o piso de gráfico é 3:1'),
    ('texto secundário', '#64748B', '#627289', 'sobre o fundo #F4F6F8 dava 4,39:1; o piso de texto é 4,5:1'),
    ('vermelho (pânico e erro)', '#D64545', '#D23535', 'como texto, e com texto branco em cima, dava 4,38:1'),
    ('variação verde do ícone', '#1B7168', '—', 'o ponto dourado sobre o verde dava 2,57:1; o ícone fica só no azul'),
]

# (foreground, background, minimum, label)
PAIRS = [
    ('text', 'bg', 4.5, 'texto sobre o fundo'),
    ('text', 'surface', 4.5, 'texto sobre cartão'),
    ('muted', 'bg', 4.5, 'texto secundário sobre o fundo'),
    ('muted', 'surface', 4.5, 'texto secundário sobre cartão'),
    ('brand', 'surface', 4.5, 'azul da marca como texto e link'),
    ('onBrand', 'brand', 4.5, 'texto sobre o azul da marca'),
    ('onAction', 'action', 4.5, 'texto no botão de ação'),
    ('action', 'bg', 3.0, 'botão de ação sobre o fundo'),
    ('onAccent', 'accent', 4.5, 'texto sobre o dourado (selo)'),
    ('accentText', 'surface', 4.5, 'dourado como texto'),
    ('accentGraphic', 'surface', 3.0, 'dourado como gráfico sobre cartão'),
    ('accentGraphic', 'bg', 3.0, 'dourado como gráfico sobre o fundo'),
    ('danger', 'surface', 4.5, 'pânico e erro como texto'),
    ('onDanger', 'danger', 4.5, 'texto no botão de pânico'),
    ('control', 'surface', 3.0, 'borda de caixa e campo'),
    ('text', 'navStrong', 4.5, 'menu do painel'),
    ('muted', 'navSoft', 4.5, 'texto secundário no menu do painel'),
]

MARK_PAIRS = [
    ('white', 'navy', 3.0, 'arco branco no ícone'),
    ('gold', 'navy', 3.0, 'ponto dourado no ícone'),
]

def report():
    rows = []
    for mode, t in TOKENS.items():
        for fg, bg, minimum, label in PAIRS:
            rows.append((mode, fg, bg, minimum, label, contrast(t[fg], t[bg])))
    for fg, bg, minimum, label in MARK_PAIRS:
        rows.append(('mark', fg, bg, minimum, label, contrast(MARK[fg], MARK[bg])))
    return rows

if __name__ == '__main__':
    fails = 0
    for mode, fg, bg, minimum, label, ratio in report():
        ok = ratio >= minimum
        fails += not ok
        print(f"{mode:5} {fg:>13}/{bg:<9} {ratio:5.2f} (min {minimum:g}) {'OK' if ok else 'FAIL'}  {label}")
    print('fails:', fails)
    raise SystemExit(1 if fails else 0)
