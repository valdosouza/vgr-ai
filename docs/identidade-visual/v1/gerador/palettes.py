"""Three VGR directions (round 23, decision 254) — light and dark tokens."""

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

# Token roles: bg (page), surface (cards), text, muted (secondary text),
# primary (brand, buttons, links), onPrimary, accent (fill: the protected one,
# highlights), onAccent, accentText (accent used AS text on surface),
# control (checkbox/field borders, >= 3:1), divider (decorative), danger.
DIRECTIONS = {
    'A': {
        'name': 'Vigília', 'font': 'Atkinson Hyperlegible Next',
        'light': dict(bg='#F3F5FA', surface='#FFFFFF', text='#131D33', muted='#4B5670', primary='#1D3A6E', onPrimary='#FFFFFF',
                      accent='#F0B03F', onAccent='#131D33', accentGraphic='#C17C0E', accentText='#8A5200', control='#7C869E', divider='#DCE1EC', danger='#B3261E'),
        'dark': dict(bg='#0A1120', surface='#111A2D', text='#E9EDF6', muted='#A9B3C9', primary='#93B6FF', onPrimary='#0A1120',
                     accent='#F3BA55', onAccent='#0A1120', accentGraphic='#F3BA55', accentText='#F3BA55', control='#7D88A3', divider='#243049', danger='#FFB4AB'),
    },
    'B': {
        'name': 'Vínculo', 'font': 'Figtree',
        'light': dict(bg='#F2F7F5', surface='#FFFFFF', text='#0F2D29', muted='#46605A', primary='#0B5E54', onPrimary='#FFFFFF',
                      accent='#F2A35E', onAccent='#0F2D29', accentGraphic='#C46A1C', accentText='#94480A', control='#73908A', divider='#D3E3DE', danger='#B3261E'),
        'dark': dict(bg='#081513', surface='#0F201D', text='#E3F1ED', muted='#9DBDB5', primary='#5CCDBB', onPrimary='#05201C',
                     accent='#F4AE72', onAccent='#081513', accentGraphic='#F4AE72', accentText='#F4AE72', control='#6F918A', divider='#1F3833', danger='#FFB4AB'),
    },
    'C': {
        'name': 'Assinatura', 'font': 'Lexend',
        'light': dict(bg='#F5F4FA', surface='#FFFFFF', text='#1F1A38', muted='#55506F', primary='#463B9C', onPrimary='#FFFFFF',
                      accent='#7BD3AE', onAccent='#1F1A38', accentGraphic='#2E9E73', accentText='#1C6A4C', control='#837DA1', divider='#DDDAEB', danger='#B3261E'),
        'dark': dict(bg='#100E1C', surface='#18152B', text='#ECEAF6', muted='#ACA7C6', primary='#AFA3FF', onPrimary='#141129',
                     accent='#7BD3AE', onAccent='#100E1C', accentGraphic='#7BD3AE', accentText='#7BD3AE', control='#837DA1', divider='#2C2848', danger='#FFB4AB'),
    },
}

# accentGraphic: the accent as a graphic on surface (>= 3:1); the pale accent
# is only ever a fill behind onAccent text.
# (foreground token, background token, minimum, what it is)
PAIRS = [
    ('text', 'bg', 4.5, 'texto sobre o fundo'),
    ('text', 'surface', 4.5, 'texto sobre cartão'),
    ('muted', 'surface', 4.5, 'texto secundário'),
    ('primary', 'surface', 4.5, 'link e destaque em texto'),
    ('onPrimary', 'primary', 4.5, 'texto no botão principal'),
    ('onAccent', 'accent', 4.5, 'texto sobre o destaque'),
    ('accentText', 'surface', 4.5, 'destaque usado como texto'),
    ('danger', 'surface', 4.5, 'erro e pânico'),
    ('control', 'surface', 3.0, 'borda de caixa e campo'),
    ('accentGraphic', 'surface', 3.0, 'destaque gráfico (ícone, marca)'),
]

def report():
    rows = []
    for key, d in DIRECTIONS.items():
        for mode in ('light', 'dark'):
            t = d[mode]
            for fg, bg, minimum, label in PAIRS:
                ratio = contrast(t[fg], t[bg])
                rows.append((key, mode, fg, bg, minimum, label, ratio))
    return rows

if __name__ == '__main__':
    fails = 0
    for key, mode, fg, bg, minimum, label, ratio in report():
        ok = ratio >= minimum
        fails += not ok
        if not ok or ratio < minimum + 0.4:
            print(f"{key} {mode:5} {fg:>10}/{bg:<8} {ratio:5.2f} (min {minimum}) {'OK' if ok else 'FAIL'}")
    print('fails:', fails)
