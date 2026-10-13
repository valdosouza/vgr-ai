"""The VGR mark in vector (decision 261): symbol, logo lockups and icons.

The symbol is direction A's: an arc that covers a lit dot, someone keeping
watch over the one kept safe. Its proportions follow Valdo's board; the
letters are Atkinson Hyperlegible Next outlines, so no file needs the font.
"""
import math, os
from glyphs import outline
from tokens import TOKENS, MARK

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')        # fetched by fetch_fonts.sh, not committed
BOLD = os.path.join(FONTS, 'atkinson-800.ttf')
REGULAR = os.path.join(FONTS, 'atkinson-400.ttf')
DESCRIPTOR = 'Vigilância e Recompensa'

# Symbol geometry, in a 100-unit box: an annulus cut flat a little below its
# centre (the arc), and the dot hanging just below the centre.
CX, CY = 50.0, 50.0
R_OUT, R_IN = 42.0, 23.5
CUT = 6.7                  # flat ends, this far below the centre
DOT_R, DOT_DY = 12.7, 3.8
SOFT = 2.4                 # same-colour stroke that softens the corners (253)
BBOX = (CX - R_OUT - SOFT / 2, CY - R_OUT - SOFT / 2, CX + R_OUT + SOFT / 2, CY + DOT_DY + DOT_R)

def _f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')

def arc_path():
    yo = CY + CUT
    xo = math.sqrt(R_OUT ** 2 - CUT ** 2)
    xi = math.sqrt(R_IN ** 2 - CUT ** 2)
    return (f'M{_f(CX - xo)} {_f(yo)}A{_f(R_OUT)} {_f(R_OUT)} 0 1 1 {_f(CX + xo)} {_f(yo)}'
            f'L{_f(CX + xi)} {_f(yo)}A{_f(R_IN)} {_f(R_IN)} 0 1 0 {_f(CX - xi)} {_f(yo)}Z')

def symbol(arc, dot):
    """The symbol's shapes in the 100-unit box."""
    return (f'<path d="{arc_path()}" fill="{arc}" stroke="{arc}" stroke-width="{SOFT}" stroke-linejoin="round"/>'
            f'<circle cx="{_f(CX)}" cy="{_f(CY + DOT_DY)}" r="{DOT_R}" fill="{dot}"/>')

def _svg(vb, inner, label, cls, standalone):
    xmlns = ' xmlns="http://www.w3.org/2000/svg"' if standalone else ''
    c = f' class="{cls}"' if cls else ''
    return f'<svg{xmlns} viewBox="{vb}" role="img" aria-label="{label}"{c}>{inner}</svg>'

def symbol_svg(arc, dot, cls='', standalone=False, pad=2.0):
    x0, y0, x1, y1 = BBOX
    vb = f'{_f(x0 - pad)} {_f(y0 - pad)} {_f(x1 - x0 + 2 * pad)} {_f(y1 - y0 + 2 * pad)}'
    return _svg(vb, symbol(arc, dot), 'Símbolo VGR', cls, standalone)

def _placed(arc, dot, x, y, height):
    """The symbol scaled so its bbox is `height` tall, top-left at (x, y)."""
    x0, y0, x1, y1 = BBOX
    s = height / (y1 - y0)
    return f'<g transform="translate({_f(x - x0 * s)} {_f(y - y0 * s)}) scale({_f(s)})">{symbol(arc, dot)}</g>', (x1 - x0) * s

COLORS = {
    # arc, dot, word, descriptor
    'claro': (TOKENS['light']['brand'], TOKENS['light']['accentGraphic'], TOKENS['light']['brand'], TOKENS['light']['brand']),
    'escuro': (TOKENS['dark']['brand'], TOKENS['dark']['accentGraphic'], TOKENS['dark']['text'], TOKENS['dark']['muted']),
    'negativo': (MARK['white'], MARK['gold'], MARK['white'], MARK['white']),
    'mono': ('currentColor',) * 4,
}

def logo_horizontal(variant, cls='logo', standalone=False):
    arc, dot, word, desc = COLORS[variant]
    size = 100
    w, ww, cap, _ = outline(BOLD, 'VGR', size, 0.01)
    # descriptor set to the exact width of the word
    probe, pw, _, _ = outline(REGULAR, DESCRIPTOR, 10, 0.005)
    dsize = 10 * ww / pw
    d, dw, dcap, _ = outline(REGULAR, DESCRIPTOR, dsize, 0.005)
    sym_h = cap * 1.51
    top = 0.0
    cap_top = top + cap * 0.29
    base = cap_top + cap
    sym, sym_w = _placed(arc, dot, 0, top, sym_h)
    gap = cap * 0.22
    wx = sym_w + gap
    dbase = base + cap * 0.40
    height = max(top + sym_h, dbase + dsize * 0.25) + 2
    width = wx + ww + 2
    inner = (sym + f'<path transform="translate({_f(wx)} {_f(base)})" d="{w}" fill="{word}"/>'
             f'<path transform="translate({_f(wx)} {_f(dbase)})" d="{d}" fill="{desc}"/>')
    return _svg(f'0 0 {_f(width)} {_f(height)}', inner, f'VGR — {DESCRIPTOR}', cls, standalone)

def logo_vertical(variant, cls='logo', standalone=False):
    arc, dot, word, desc = COLORS[variant]
    size = 100
    w, ww, cap, _ = outline(BOLD, 'VGR', size, 0.01)
    probe, pw, _, _ = outline(REGULAR, DESCRIPTOR, 10, 0.005)
    dsize = 10 * ww * 1.05 / pw
    d, dw, _, _ = outline(REGULAR, DESCRIPTOR, dsize, 0.005)
    width = max(ww, dw) + 4
    sym_h = cap * 1.4
    x0, y0, x1, y1 = BBOX
    sym_w = (x1 - x0) * sym_h / (y1 - y0)
    sym, _ = _placed(arc, dot, (width - sym_w) / 2, 0, sym_h)
    base = sym_h + cap * 0.45 + cap
    dbase = base + cap * 0.42
    inner = (sym + f'<path transform="translate({_f((width - ww) / 2)} {_f(base)})" d="{w}" fill="{word}"/>'
             f'<path transform="translate({_f((width - dw) / 2)} {_f(dbase)})" d="{d}" fill="{desc}"/>')
    return _svg(f'0 0 {_f(width)} {_f(dbase + dsize * 0.25 + 2)}', inner, f'VGR — {DESCRIPTOR}', cls, standalone)

def _icon_symbol(scale_of_canvas, arc, dot, canvas=108):
    """Symbol centred on its bbox, its width `scale_of_canvas` of the canvas."""
    x0, y0, x1, y1 = BBOX
    s = canvas * scale_of_canvas / (x1 - x0)
    tx = canvas / 2 - (x0 + x1) / 2 * s
    ty = canvas / 2 - (y0 + y1) / 2 * s
    return f'<g transform="translate({_f(tx)} {_f(ty)}) scale({_f(s)})">{symbol(arc, dot)}</g>'

# Android adaptive icons show a 72-unit circle of the 108 canvas and keep a
# 66-unit circle safe under every mask: the symbol's corners must stay inside.
def _adaptive_scale():
    x0, y0, x1, y1 = BBOX
    half_diag = math.hypot((x1 - x0) / 2, (y1 - y0) / 2)
    return 33 / half_diag * (x1 - x0) / 108

ADAPTIVE = _adaptive_scale()
FULL = 0.60                # iOS and store: the board's proportion
FAVICON = 0.76             # browser tab: the symbol as large as it fits

def icon_svg(mask='square', cls='appicon', standalone=False, uid='i'):
    """The app icon as shown under a launcher mask: navy, white arc, gold dot."""
    scale = {'square': FULL, 'none': FULL, 'circle': ADAPTIVE, 'favicon': FAVICON}[mask]
    inner_sym = _icon_symbol(scale, MARK['white'], MARK['gold'])
    clip = {'square': '<rect width="108" height="108" rx="24"/>',
            'circle': '<circle cx="54" cy="54" r="54"/>',
            'favicon': '<rect width="108" height="108" rx="20"/>',
            'none': '<rect width="108" height="108"/>'}[mask]
    cid = f'clip-{mask}-{uid}'
    return _svg('0 0 108 108', f'<defs><clipPath id="{cid}">{clip}</clipPath></defs>'
                f'<g clip-path="url(#{cid})"><rect width="108" height="108" fill="{MARK["navy"]}"/>{inner_sym}</g>',
                'Ícone do app VGR', cls, standalone)

def adaptive_foreground_svg():
    """Android adaptive icon, foreground layer (the background layer is the navy)."""
    return _svg('0 0 108 108', _icon_symbol(ADAPTIVE, MARK['white'], MARK['gold']), 'Ícone do app VGR — frente', '', True)

def themed_svg(color='#000000', cls='', standalone=False):
    """Android 13+ themed icon: one colour; the system tints it."""
    return _svg('0 0 108 108', _icon_symbol(ADAPTIVE, color, color), 'Ícone temático do VGR', cls, standalone)

def pattern_svg(stroke, highlight_arc, highlight_dot, cls='pattern', uid='p'):
    """The board's pattern of arcs: a quiet field with one lit arc."""
    cells = []
    for row in range(3):
        for col in range(6):
            x, y = col * 100 + (50 if row % 2 else 0), row * 70
            lit = (row, col) == (1, 3)
            arc = highlight_arc if lit else stroke
            dot = highlight_dot if lit else 'none'
            cells.append(f'<g transform="translate({x - 50} {y - 20})">'
                         f'<path d="{arc_path()}" fill="{arc}" stroke="{arc}" stroke-width="{SOFT}" stroke-linejoin="round"/>'
                         + (f'<circle cx="{_f(CX)}" cy="{_f(CY + DOT_DY)}" r="{DOT_R}" fill="{dot}"/>' if lit else '')
                         + '</g>')
    return _svg('0 0 560 190', f'<defs><clipPath id="{uid}"><rect width="560" height="190" rx="14"/></clipPath></defs>'
                f'<g clip-path="url(#{uid})">{"".join(cells)}</g>', 'Padrão de arcos', cls, False)

def write_files(out):
    os.makedirs(out, exist_ok=True)
    files = {
        'simbolo.svg': symbol_svg(TOKENS['light']['brand'], TOKENS['light']['accentGraphic'], standalone=True),
        'simbolo-negativo.svg': symbol_svg(MARK['white'], MARK['gold'], standalone=True),
        'logo-horizontal-claro.svg': logo_horizontal('claro', standalone=True),
        'logo-horizontal-escuro.svg': logo_horizontal('escuro', standalone=True),
        'logo-horizontal-negativo.svg': logo_horizontal('negativo', standalone=True),
        'logo-horizontal-mono.svg': logo_horizontal('mono', standalone=True),
        'logo-vertical-claro.svg': logo_vertical('claro', standalone=True),
        'logo-vertical-negativo.svg': logo_vertical('negativo', standalone=True),
        'icone.svg': icon_svg('none', standalone=True, uid='f'),
        'icone-android-frente.svg': adaptive_foreground_svg(),
        'favicon.svg': icon_svg('favicon', standalone=True, uid='fav'),
        'icone-tematico.svg': themed_svg(standalone=True),
    }
    for name, svg in files.items():
        with open(os.path.join(out, name), 'w') as fh:
            fh.write(svg + '\n')
    return sorted(files)
