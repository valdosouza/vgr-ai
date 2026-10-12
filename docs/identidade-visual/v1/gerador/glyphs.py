"""Text to SVG outlines from the real font files (no font needed to view)."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

_cache = {}

def _font(path):
    if path not in _cache:
        f = TTFont(path)
        _cache[path] = (f, f.getGlyphSet(), f.getBestCmap(), f['head'].unitsPerEm)
    return _cache[path]

def _fmt(v):
    return f"{v:.2f}".rstrip('0').rstrip('.')

def outline(path, text, size, tracking=0.0):
    """(d, width, cap_height, boxes) for `text` at `size` px, baseline y=0,
    y down. `tracking` in em. boxes: (char, x0, y0, x1, y1)."""
    font, gs, cmap, upem = _font(path)
    s = size / upem
    x = 0.0
    parts, boxes = [], []
    for i, ch in enumerate(text):
        glyph = gs[cmap[ord(ch)]]
        pen = SVGPathPen(gs, ntos=_fmt)
        glyph.draw(TransformPen(pen, (s, 0, 0, -s, x, 0)))
        parts.append(pen.getCommands())
        bp = BoundsPen(gs)
        glyph.draw(bp)
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            boxes.append((ch, x + x0 * s, -y1 * s, x + x1 * s, -y0 * s))
        x += glyph.width * s + (tracking * size if i < len(text) - 1 else 0)
    cap = font['OS/2'].sCapHeight * s
    return ' '.join(p for p in parts if p), x, cap, boxes
