"""Builds VGR identity V1 (round 23): SVG files + the presentation page."""
import html, os
from palettes import DIRECTIONS, PAIRS, contrast
from glyphs import outline

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')   # OFL TTFs, fetched by fetch_fonts.sh (not committed)
OUT = os.path.dirname(HERE)            # docs/identidade-visual/v1
SLUG = {'A': 'a-vigilia', 'B': 'b-vinculo', 'C': 'c-assinatura'}
FONTFILE = {'A': ('atkinson-700', 'atkinson-400'), 'B': ('figtree-800', 'figtree-400'), 'C': ('lexend-600', 'lexend-400')}
TRACK = {'A': 0.06, 'B': 0.03, 'C': 0.04}
CSSFONT = {'A': "'Atkinson Hyperlegible Next', system-ui, sans-serif",
           'B': "'Figtree', system-ui, sans-serif",
           'C': "'Lexend', system-ui, sans-serif"}

def font(key, weight):
    return os.path.join(FONTS, FONTFILE[key][0 if weight == 'bold' else 1] + '.ttf')

# ---------------------------------------------------------------- symbols
def symbol_a(main, accent):
    # Vigília: someone watching over (the arc) the one kept safe (the warm dot).
    return (f'<path d="M21.8 70.3A30 30 0 1 1 78.2 70.3" fill="none" stroke="{main}" stroke-width="10" stroke-linecap="round"/>'
            f'<circle cx="50" cy="66" r="10" fill="{accent}"/>')

def symbol_b(main, accent):
    # Vínculo: two people who come close to help the one in need — the V.
    return (f'<path d="M26 28Q33 56 50 74M74 28Q67 56 50 74" fill="none" stroke="{main}" stroke-width="9" stroke-linecap="round"/>'
            f'<circle cx="26" cy="28" r="9" fill="{main}"/><circle cx="74" cy="28" r="9" fill="{main}"/>'
            f'<circle cx="50" cy="74" r="11" fill="{accent}"/>')

def _g_dot(boxes, size):
    _, x0, y0, x1, y1 = [b for b in boxes if b[0] == 'G'][0]
    w, h = x1 - x0, y1 - y0
    # Inside the counter, clear of the bar that enters from the right.
    return x0 + w * 0.37, y0 + h * 0.5, h * 0.095

def symbol_c(main, accent, size=100):
    # Assinatura: the G of VGR holds someone inside (the dot).
    d, w, cap, boxes = outline(font('C', 'bold'), 'G', size)
    cx, cy, r = _g_dot(boxes, size)
    _, x0, y0, x1, y1 = boxes[0]
    pad = 8
    vb = f"{x0 - pad:.1f} {y0 - pad:.1f} {x1 - x0 + 2 * pad:.1f} {y1 - y0 + 2 * pad:.1f}"
    return vb, f'<path d="{d}" fill="{main}"/><circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{accent}"/>'

def symbol_svg(key, main, accent, cls=''):
    if key == 'C':
        vb, inner = symbol_c(main, accent)
    else:
        vb, inner = '0 0 100 100', (symbol_a if key == 'A' else symbol_b)(main, accent)
    return f'<svg class="{cls}" viewBox="{vb}" role="img" aria-label="Símbolo VGR">{inner}</svg>'

# ---------------------------------------------------------------- logo lockup
def logo_svg(key, mode, standalone=False):
    t = DIRECTIONS[key][mode]
    main = t['primary']
    accent = t['accentGraphic']
    word, ww, cap, boxes = outline(font(key, 'bold'), 'VGR', 72, TRACK[key])
    desc, dw, dcap, _ = outline(font(key, 'regular'), 'Vigilância e Recompensa', 17, 0.01)
    parts = []
    if key == 'C':
        cx, cy, r = _g_dot(boxes, 72)
        parts.append(f'<g transform="translate(0 72)"><path d="{word}" fill="{t["text"]}"/>'
                     f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{accent}"/></g>')
        parts.append(f'<g transform="translate(2 104)"><path d="{desc}" fill="{t["muted"]}"/></g>')
        width, height = max(ww, dw) + 6, 112
    else:
        sym = (symbol_a if key == 'A' else symbol_b)(main, accent)
        parts.append(f'<g transform="translate(0 6) scale(0.92)">{sym}</g>')
        parts.append(f'<g transform="translate(104 72)"><path d="{word}" fill="{t["text"]}"/></g>')
        parts.append(f'<g transform="translate(106 104)"><path d="{desc}" fill="{t["muted"]}"/></g>')
        width, height = 104 + max(ww, dw) + 6, 112
    xmlns = ' xmlns="http://www.w3.org/2000/svg"' if standalone else ''
    label = f'VGR — Vigilância e Recompensa'
    return (f'<svg{xmlns} viewBox="0 0 {width:.0f} {height}" role="img" aria-label="{label}" class="logo">'
            + ''.join(parts) + '</svg>')

# ---------------------------------------------------------------- app icon
def icon_svg(key, standalone=False, mask='square'):
    """Adaptive icon: 108 canvas, content inside the 66 safe zone."""
    t = DIRECTIONS[key]['light']
    bg = t['primary']
    if key == 'C':
        word, ww, cap, boxes = outline(font('C', 'bold'), 'VGR', 30, 0.04)
        cx, cy, r = _g_dot(boxes, 30)
        x = 54 - ww / 2
        y = 54 + cap / 2
        content = (f'<g transform="translate({x:.2f} {y:.2f})"><path d="{word}" fill="#FFFFFF"/>'
                   f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{t["accent"]}"/></g>')
    else:
        sym = (symbol_a if key == 'A' else symbol_b)('#FFFFFF', t['accent'])
        content = f'<g transform="translate(25 24) scale(0.58)">{sym}</g>'
    clip = ('<rect width="108" height="108" rx="26"/>' if mask == 'square' else '<circle cx="54" cy="54" r="54"/>')
    cid = f'clip-{key}-{mask}-{"s" if standalone else "i"}'
    xmlns = ' xmlns="http://www.w3.org/2000/svg"' if standalone else ''
    return (f'<svg{xmlns} viewBox="0 0 108 108" role="img" aria-label="Ícone do app VGR" class="appicon">'
            f'<defs><clipPath id="{cid}">{clip}</clipPath></defs>'
            f'<g clip-path="url(#{cid})"><rect width="108" height="108" fill="{bg}"/>{content}</g></svg>')

# ---------------------------------------------------------------- phone screens
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BACK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PLUS = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'

def phone_vars(key, mode):
    t = DIRECTIONS[key][mode]
    return ';'.join(f'--{k}:{v}' for k, v in t.items()) + f";--font:{CSSFONT[key]}"

def box(checked):
    return f'<span class="cb{" on" if checked else ""}">{CHECK if checked else ""}</span>'

def screen_feed(key, mode):
    t = DIRECTIONS[key][mode]
    mark = symbol_svg(key, t['primary'], t['accentGraphic'], 'mark')
    items = [
        ('Roubo / furto · Criança', '~1 km · há 15 min', ''),
        ('Atividade suspeita · Veículo', '~2 km · há 40 min', ''),
        ('Sequestro · Criança', '~5 km · hoje', 'risco alto: posição e horário aproximados'),
        ('Vandalismo · Praça', '~3 km · ontem', ''),
    ]
    rows = ''.join(f'<li class="card"><b>{a}</b><span class="mut">{b}</span>{f"<span class=note>{c}</span>" if c else ""}</li>' for a, b, c in items)
    return (f'<div class="bar">{mark}<span class="h">Por perto</span></div>'
            f'<div class="chip">Mais recentes</div><ul class="list">{rows}</ul>'
            f'<div class="fab">{PLUS}<span>Denunciar</span></div>')

def screen_detail(key, mode):
    dirs = ['Norte', 'Nordeste', 'Leste', 'Sudeste', 'Sul', 'Sudoeste', 'Oeste', 'Noroeste']
    chips = ''.join(f'<span class="dir{" sel" if d == "Leste" else ""}">{d}</span>' for d in dirs)
    return (f'<div class="bar">{BACK}<span class="h">Denúncia</span></div>'
            f'<div class="pad"><div class="title">Roubo / furto · Criança</div>'
            f'<div class="row"><span class="pill">Aberta</span><span class="mut">~1 km · há 15 min</span></div>'
            f'<div class="sec">Linha do tempo</div>'
            f'<div class="tl"><span class="dot"></span><span>Denúncia registrada</span><span class="mut">14:02</span></div>'
            f'<div class="tl"><span class="dot"></span><span>Alguém ofereceu ajuda</span><span class="mut">14:09</span></div>'
            f'<div class="sec">Em que direção você viu a pessoa ir?</div><div class="dirs">{chips}</div>'
            f'<div class="btn">Oferecer ajuda</div></div>')

def screen_offer(key, mode):
    types = [('Presença física', True), ('Repassar informação', False), ('Apoio remoto', False), ('Divulgar', True), ('Contribuição financeira', False)]
    rows = ''.join(f'<li>{box(c)}<span>{n}</span></li>' for n, c in types)
    return (f'<div class="bar">{BACK}<span class="h">Oferecer ajuda</span></div>'
            f'<div class="pad"><div class="sec first">Como você quer ajudar?</div><ul class="checks">{rows}</ul>'
            f'<div class="card name"><div class="namerow">{box(False)}<b>Mostrar meu nome a quem denunciou</b></div>'
            f'<p>Na dúvida, deixe desmarcado: uma denúncia pode ser falsa, feita só para descobrir quem ajuda. '
            f'Sem o nome você continua podendo conversar, ser avaliado e receber recompensa.</p></div>'
            f'<div class="btn">Enviar oferta</div></div>')

def phone(key, mode, which):
    body = {'feed': screen_feed, 'detail': screen_detail, 'offer': screen_offer}[which](key, mode)
    label = {'feed': 'Por perto', 'detail': 'Denúncia', 'offer': 'Oferecer ajuda'}[which]
    return (f'<figure class="phone-wrap"><div class="phone" style="{phone_vars(key, mode)}">'
            f'<div class="status"><span>9:41</span></div>{body}</div>'
            f'<figcaption>{label} · {"claro" if mode == "light" else "escuro"}</figcaption></figure>')

# ---------------------------------------------------------------- page pieces
CONCEPT = {
    'A': ('Vigília', 'Velar por alguém',
          'Um arco que cobre e um ponto aceso embaixo dele: alguém que fica de vigia para que o outro esteja seguro. É a leitura de "vigiar" como cuidado. A luz quente do ponto é a pessoa protegida, e o azul profundo é a noite em que a vigília acontece. O escuro vem primeiro, porque é quando mais se precisa.'),
    'B': ('Vínculo', 'Quem está perto se aproxima',
          'Duas pessoas que se aproximam de uma terceira e formam o V de VGR e de vigiar. É o vínculo 1:1, 1:N ou N:N do objetivo 4, e a ajuda que vem de quem está perto (decisão 2). O verde-petróleo traz cuidado e confiança. O ponto quente embaixo é quem recebe a ajuda.'),
    'C': ('Assinatura', 'O nome como símbolo',
          'A marca é o próprio nome. O G de VGR guarda alguém dentro dele: um ponto protegido no meio da letra. É a direção mais discreta, porque na tela inicial parece só uma sigla. O índigo dá firmeza e confiança, e o verde-menta é o cuidado.'),
}
MAP = {
    'A': [('Símbolo', 'arco que cobre + ponto aceso: vigiar como velar por', '250, 252, 6, 55'),
          ('Ponto quente', 'quem é protegido; o destaque é raro, como a recompensa', '1, 30, 237, 238'),
          ('Azul noturno', 'calma, confiança; escuro desenhado primeiro', '253, 256'),
          ('Atkinson Hyperlegible Next', 'feita para baixa visão (Braille Institute), OFL', '255, 257'),
          ('Ícone', 'forma abstrata, nada de olho, sirene ou distintivo', '252'),
          ('Telas', 'posição e horário aproximados no risco alto; nome desmarcado por padrão', '135, 41, 237')],
    'B': [('Símbolo', 'duas pessoas se aproximando de uma: o V', '250, obj. 4, 2, 5'),
          ('Ponto quente', 'quem recebe a ajuda; o destaque é raro', '1, 30, 237'),
          ('Verde-petróleo', 'cuidado e confiança, sem tom policial', '253, 252'),
          ('Figtree', 'humanista e arredondada, OFL', '255, 253'),
          ('Ícone', 'forma de conexão, não diz "denúncia"', '252'),
          ('Telas', 'cinco frentes de ajuda iguais; nome desmarcado por padrão', '10, 208, 237')],
    'C': [('Símbolo', 'o nome; o G guarda alguém dentro', '250, 252, 55'),
          ('Ponto menta', 'cuidado e proteção, discreto', '253, 6'),
          ('Índigo', 'firmeza e integridade (duplo controle, responsabilização)', '23, 45, 253'),
          ('Lexend', 'criada para fluência de leitura, OFL', '255, 257'),
          ('Ícone', 'só a sigla: a mais discreta das três', '252, 238'),
          ('Telas', 'mesma linguagem no painel sóbrio', '258, 133')],
}
COMPARE = [
    ('Leitura de "vigiar"', 'Direta: a vigília, velar por alguém', 'Indireta: o V das pessoas que se aproximam', 'No nome: o G que guarda'),
    ('O vínculo entre pessoas', 'Implícito (quem cuida e quem é cuidado)', 'Explícito: é o próprio símbolo', 'Implícito'),
    ('Discrição na tela inicial', 'Alta: forma abstrata', 'Alta: forma de conexão', 'Máxima: só a sigla'),
    ('Legibilidade da fonte', 'A maior: feita para baixa visão', 'Boa', 'Muito boa: feita para leitura'),
    ('Funciona pequeno (ícone 48 dp)', 'Muito bem: duas formas simples', 'Bem: cinco formas', 'Razoável: três letras'),
    ('Risco', 'Arco e ponto podem lembrar um nascer do sol genérico', 'Pode lembrar marcas de rede e conexão', 'Sigla pura diz pouco sem o app aberto'),
]
PRINCIPLES = [
    ('Velar, não espionar', 'Nada de olho, sirene, distintivo, mira ou radar.', '250, 252'),
    ('O centro são as pessoas', 'Quem denuncia e quem ajuda, em 1:1, 1:N ou N:N.', 'obj. 4, 2'),
    ('Perto importa', 'A ajuda vem de quem está próximo.', '2, 7, 135'),
    ('Quem ajuda escolhe como', 'Cinco frentes, nenhuma vale mais.', '5, 10, 208'),
    ('Proteção antes da exposição', 'Anonimato como padrão; nada depende de rosto ou nome.', '6, 40, 55, 170, 237, 238'),
    ('Recompensa opcional', 'Destaque raro; nada de moeda, cifrão ou troféu.', '1, 30, 247'),
    ('Confiável e acolhedora', 'Formas arredondadas, cores calmas; vermelho só para pânico e erro.', '51, 253'),
    ('Discreta na tela', 'No aparelho, só "VGR" e um símbolo abstrato.', '252'),
    ('Legível no pior momento', 'WCAG AA, toque de 48 dp, texto até 200%.', '257'),
    ('A noite é cenário real', 'O escuro desenhado junto com o claro.', '256'),
    ('Fonte dentro do app', 'Licença OFL; nunca baixada em tempo de execução.', '255'),
    ('Um sistema, dois apps', 'Tokens no vgr_widgets; painel em versão sóbria.', '133, 258'),
]

def swatches(key):
    out = []
    for mode in ('light', 'dark'):
        t = DIRECTIONS[key][mode]
        cells = ''.join(f'<div class="sw"><span class="c" style="background:{t[k]}"></span><span class="k">{k}</span><code>{t[k]}</code></div>'
                        for k in ('bg', 'surface', 'text', 'muted', 'primary', 'accent', 'accentGraphic', 'control', 'danger'))
        rows = []
        for fg, bg, minimum, label in PAIRS:
            r = contrast(t[fg], t[bg])
            rows.append(f'<tr><td><span class="pair" style="background:{t[bg]};color:{t[fg]}">Aa</span></td><td>{label}</td>'
                        f'<td class="num">{r:.1f}:1</td><td class="num">mín. {minimum:g}</td><td>{"passa" if r >= minimum else "FALHA"}</td></tr>')
        out.append(f'<div class="palette"><h4>{"Claro" if mode == "light" else "Escuro"}</h4><div class="sws">{cells}</div>'
                   f'<div class="tbl"><table><thead><tr><th></th><th>Par</th><th>Contraste</th><th>Piso</th><th></th></tr></thead>'
                   f'<tbody>{"".join(rows)}</tbody></table></div></div>')
    return ''.join(out)

def home_screen(key):
    other = lambda label, glyph: f'<div class="app"><span class="gen">{glyph}</span><span>{label}</span></div>'
    cal = '<svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="15" rx="3" fill="none" stroke="#fff" stroke-width="2"/><path d="M4 10h16M9 3v4M15 3v4" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>'
    notes = '<svg viewBox="0 0 24 24"><path d="M7 8h10M7 12h10M7 16h6" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>'
    sun = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="5" fill="none" stroke="#fff" stroke-width="2"/></svg>'
    return (f'<div class="home">{other("Agenda", cal)}{other("Notas", notes)}'
            f'<div class="app">{icon_svg(key)}<span>VGR</span></div>{other("Clima", sun)}</div>')

def direction_section(key):
    d = DIRECTIONS[key]
    name, tagline, text = CONCEPT[key]
    phones_light = ''.join(phone(key, 'light', w) for w in ('feed', 'detail', 'offer'))
    phones_dark = ''.join(phone(key, 'dark', w) for w in ('feed', 'detail', 'offer'))
    maprows = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td class="refs">{c}</td></tr>' for a, b, c in MAP[key])
    lt, dk = d['light'], d['dark']
    return f'''
<section class="direction" id="dir-{key.lower()}" aria-labelledby="h-{key}">
  <header class="dhead">
    <span class="letter">{key}</span>
    <div><h2 id="h-{key}">{name}</h2><p class="tag">{tagline}</p></div>
  </header>
  <p class="concept">{text}</p>
  <div class="grid2">
    <div class="tile" style="background:{lt['bg']}">{logo_svg(key, 'light')}</div>
    <div class="tile" style="background:{dk['bg']}">{logo_svg(key, 'dark')}</div>
  </div>
  <div class="grid3">
    <div class="block"><h3>Ícone do app</h3>
      <div class="icons">{icon_svg(key, mask='square')}{icon_svg(key, mask='circle')}</div>
      <p class="small">Máscara do iPhone e do Android. O símbolo fica dentro da área segura do ícone adaptativo.</p></div>
    <div class="block"><h3>Na tela inicial</h3>{home_screen(key)}
      <p class="small">Ao lado de outros apps, aparece só "VGR" (decisão 252).</p></div>
    <div class="block"><h3>Fonte · {d['font']}</h3>
      <div class="type" style="font-family:{CSSFONT[key]};color:var(--ink)">
        <div class="t1">Quem está perto pode ajudar</div>
        <div class="t2">Presença física, repassar informação, apoio remoto, divulgar ou contribuição financeira: quem ajuda escolhe como.</div>
        <div class="t3">0123456789 · ~1 km · há 15 min</div></div>
      <p class="small">Licença OFL; vai embutida no app (decisão 255).</p></div>
  </div>
  <h3 class="sub">Paleta e contraste calculado (WCAG AA, decisão 257)</h3>
  <div class="grid2 pal">{swatches(key)}</div>
  <h3 class="sub">Três telas reais, claro e escuro</h3>
  <div class="phones">{phones_light}</div>
  <div class="phones">{phones_dark}</div>
  <h3 class="sub">O que cada elemento representa</h3>
  <div class="tbl"><table class="map"><thead><tr><th>Elemento</th><th>O que diz</th><th>Decisões</th></tr></thead><tbody>{maprows}</tbody></table></div>
</section>'''

def page():
    principles = ''.join(f'<li><b>{a}.</b> {b} <span class="refs">{c}</span></li>' for a, b, c in PRINCIPLES)
    cmp_rows = ''.join(f'<tr><th scope="row">{r[0]}</th><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>' for r in COMPARE)
    nav = ''.join(f'<a href="#dir-{k.lower()}"><span class="mini">{icon_svg(k)}</span>{k} · {DIRECTIONS[k]["name"]}</a>' for k in 'ABC')
    sections = ''.join(direction_section(k) for k in 'ABC')
    return f'''<title>Identidade VGR</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;700&family=Figtree:wght@400;600;800&family=Lexend:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
/* Layout: one long column of three directions, each a stack of specimen blocks; page chrome stays neutral so the directions carry the color. */
:root {{
  --page:#F4F5F7; --card:#FFFFFF; --ink:#15181E; --soft:#585F6C; --line:#DCDFE5; --chip:#EAECF0; --focus:#1D3A6E;
  --chrome: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --page:#0E1014; --card:#171A20; --ink:#ECEEF2; --soft:#A3A9B4; --line:#2B2F37; --chip:#22262E; --focus:#93B6FF; color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --page:#0E1014; --card:#171A20; --ink:#ECEEF2; --soft:#A3A9B4; --line:#2B2F37; --chip:#22262E; --focus:#93B6FF; color-scheme: dark; }}
body {{ background:var(--page); color:var(--ink); font-family:var(--chrome); line-height:1.5; }}
.wrap {{ max-width:1180px; margin:0 auto; padding-inline:20px; padding-block:40px 64px; }}
a {{ color:inherit; }}
a:focus-visible {{ outline:2px solid var(--focus); outline-offset:3px; border-radius:6px; }}
.eyebrow {{ font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--soft); }}
h1 {{ font-size:clamp(30px,5vw,46px); line-height:1.08; margin:.25em 0 .3em; text-wrap:balance; letter-spacing:-.01em; }}
.lede {{ max-width:68ch; font-size:17px; color:var(--soft); margin:0; }}
.lede b {{ color:var(--ink); }}
.readings {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; margin:28px 0 8px; }}
.reading {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px; }}
.reading .big {{ font-size:22px; font-weight:700; }}
.reading .from {{ font-size:13px; color:var(--soft); }}
h2.section {{ font-size:22px; margin:44px 0 12px; }}
.principles {{ columns:2 320px; column-gap:28px; padding:0; margin:0; list-style:none; }}
.principles li {{ break-inside:avoid; padding:7px 0; border-bottom:1px solid var(--line); font-size:15px; }}
.refs {{ font-family:var(--mono); font-size:12px; color:var(--soft); white-space:nowrap; }}
.nav {{ display:flex; flex-wrap:wrap; gap:10px; margin:28px 0 0; }}
.nav a {{ display:flex; align-items:center; gap:10px; text-decoration:none; background:var(--card); border:1px solid var(--line); border-radius:999px; padding:6px 14px 6px 6px; font-weight:600; }}
.mini svg {{ width:30px; height:30px; display:block; }}
.direction {{ margin-top:56px; padding-top:28px; border-top:2px solid var(--ink); }}
.dhead {{ display:flex; gap:14px; align-items:center; }}
.letter {{ font-family:var(--mono); font-size:13px; border:1px solid var(--ink); border-radius:6px; padding:2px 8px; }}
.dhead h2 {{ font-size:30px; margin:0; line-height:1.1; }}
.tag {{ margin:2px 0 0; color:var(--soft); }}
.concept {{ max-width:70ch; font-size:16px; margin:14px 0 20px; }}
.grid2 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:14px; }}
.grid3 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px; margin-top:14px; }}
.tile {{ border-radius:16px; border:1px solid var(--line); display:flex; align-items:center; justify-content:center; padding:36px 24px; min-height:150px; }}
.tile .logo {{ width:min(100%,340px); height:auto; }}
.block {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:16px; min-width:0; }}
.block h3, h3.sub {{ font-size:13px; letter-spacing:.06em; text-transform:uppercase; color:var(--soft); margin:0 0 12px; font-weight:600; }}
h3.sub {{ margin:28px 0 12px; }}
.icons {{ display:flex; gap:16px; align-items:center; }}
.icons .appicon {{ width:88px; height:88px; }}
.small {{ font-size:13px; color:var(--soft); margin:12px 0 0; }}
.home {{ background:#33404F; border-radius:14px; padding:16px 10px 12px; display:grid; grid-template-columns:repeat(4,1fr); gap:8px; }}
.app {{ display:flex; flex-direction:column; align-items:center; gap:6px; color:#FFFFFF; font-size:11px; min-width:0; }}
.app .appicon, .gen {{ width:48px; height:48px; border-radius:12px; }}
.gen {{ background:#5B6878; display:flex; align-items:center; justify-content:center; }}
.gen svg {{ width:24px; height:24px; }}
.type .t1 {{ font-size:24px; font-weight:700; line-height:1.15; }}
.type .t2 {{ font-size:15px; margin-top:8px; }}
.type .t3 {{ font-size:14px; margin-top:8px; font-variant-numeric:tabular-nums; color:var(--soft); }}
.palette {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:16px; min-width:0; }}
.palette h4 {{ margin:0 0 10px; font-size:15px; }}
.sws {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(96px,1fr)); gap:8px; }}
.sw {{ display:flex; flex-direction:column; gap:2px; font-size:12px; }}
.sw .c {{ height:34px; border-radius:8px; border:1px solid var(--line); }}
.sw .k {{ color:var(--soft); }}
code, .num {{ font-family:var(--mono); font-size:12px; font-variant-numeric:tabular-nums; }}
.tbl {{ overflow-x:auto; margin-top:12px; }}
table {{ border-collapse:collapse; width:100%; font-size:13px; }}
th, td {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--line); vertical-align:top; }}
thead th {{ color:var(--soft); font-weight:600; }}
.pair {{ display:inline-block; padding:2px 7px; border-radius:6px; font-weight:700; border:1px solid var(--line); }}
.map th[scope=row] {{ white-space:nowrap; }}
.phones {{ display:flex; flex-wrap:wrap; gap:18px; margin-bottom:10px; }}
.phone-wrap {{ margin:0; display:flex; flex-direction:column; gap:6px; align-items:center; }}
.phone-wrap figcaption {{ font-size:12px; color:var(--soft); }}
.phone {{ width:244px; height:500px; border-radius:30px; border:7px solid #0C0D10; outline:1px solid var(--line); background:var(--bg); color:var(--text);
  font-family:var(--font); font-size:13px; position:relative; overflow:hidden; display:flex; flex-direction:column; }}
.phone .status {{ height:22px; padding:4px 16px 0; font-size:11px; font-weight:600; color:var(--text); }}
.phone .bar {{ display:flex; align-items:center; gap:8px; padding:6px 14px 10px; color:var(--text); }}
.phone .bar svg {{ width:22px; height:22px; flex:none; }}
.phone .bar .mark {{ width:24px; height:24px; }}
.phone .h {{ font-size:18px; font-weight:700; }}
.phone .chip {{ margin:0 14px 8px; align-self:flex-start; border:1px solid var(--control); color:var(--text); border-radius:999px; padding:3px 10px; font-size:12px; }}
.phone .list {{ list-style:none; margin:0; padding:0 12px; display:flex; flex-direction:column; gap:8px; }}
.phone .card {{ background:var(--surface); border:1px solid var(--divider); border-radius:14px; padding:10px 12px; display:flex; flex-direction:column; gap:2px; }}
.phone .mut {{ color:var(--muted); font-size:12px; }}
.phone .note {{ color:var(--accentText); font-size:11.5px; }}
.phone .fab {{ position:absolute; right:14px; bottom:16px; background:var(--primary); color:var(--onPrimary); border-radius:16px; padding:10px 16px 10px 12px; display:flex; gap:6px; align-items:center; font-weight:700; }}
.phone .fab svg {{ width:18px; height:18px; }}
.phone .pad {{ padding:0 14px; display:flex; flex-direction:column; gap:8px; }}
.phone .title {{ font-size:17px; font-weight:700; line-height:1.2; }}
.phone .row {{ display:flex; gap:8px; align-items:center; }}
.phone .pill {{ background:var(--accent); color:var(--onAccent); border-radius:999px; padding:2px 9px; font-size:11.5px; font-weight:700; }}
.phone .sec {{ margin-top:6px; font-size:12px; font-weight:700; color:var(--muted); }}
.phone .sec.first {{ margin-top:0; }}
.phone .tl {{ display:grid; grid-template-columns:10px 1fr auto; gap:8px; align-items:center; }}
.phone .tl .dot {{ width:8px; height:8px; border-radius:50%; background:var(--primary); }}
.phone .dirs {{ display:flex; flex-wrap:wrap; gap:5px; }}
.phone .dir {{ border:1px solid var(--control); border-radius:999px; padding:2px 8px; font-size:11px; }}
.phone .dir.sel {{ background:var(--primary); color:var(--onPrimary); border-color:var(--primary); }}
.phone .btn {{ margin-top:8px; background:var(--primary); color:var(--onPrimary); border-radius:14px; text-align:center; padding:11px; font-weight:700; }}
.phone .checks {{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:7px; }}
.phone .checks li, .phone .namerow {{ display:flex; gap:9px; align-items:center; }}
.phone .cb {{ width:20px; height:20px; border-radius:6px; border:2px solid var(--control); display:flex; align-items:center; justify-content:center; flex:none; color:var(--onPrimary); }}
.phone .cb.on {{ background:var(--primary); border-color:var(--primary); }}
.phone .cb svg {{ width:15px; height:15px; }}
.phone .name {{ gap:6px; }}
.phone .name p {{ margin:0; font-size:11.5px; color:var(--muted); line-height:1.4; }}
.compare th[scope=row] {{ width:22%; }}
.rec {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--ink); border-radius:12px; padding:16px 18px; margin-top:16px; max-width:80ch; }}
.rec p {{ margin:.3em 0; }}
.answer {{ margin-top:16px; font-size:15px; }}
footer {{ margin-top:48px; font-size:13px; color:var(--soft); }}
@media (max-width:520px) {{ .principles {{ columns:1; }} .home {{ gap:4px; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior:auto !important; }} }}
</style>
<div class="wrap">
  <p class="eyebrow">Rodada 23 · V1 · decisões 250–260</p>
  <h1>Três direções para a identidade do VGR</h1>
  <p class="lede">Cada direção traz <b>logo, ícone, paleta clara e escura com contraste calculado, fonte e três telas reais</b> do app. A última tabela de cada uma mostra quais decisões do projeto cada elemento representa (decisão 251). Escolha uma, ou combine partes de mais de uma.</p>

  <div class="readings" aria-label="As três leituras de VGR (decisão 250)">
    <div class="reading"><div class="big">vigiar</div><div class="from">as letras lidas em inglês: vi-gi-ar. Vigiar no sentido de velar por alguém (decisão 252).</div></div>
    <div class="reading"><div class="big">Vigilância e Recompensa</div><div class="from">português</div></div>
    <div class="reading"><div class="big">Vigilant and Reward</div><div class="from">inglês</div></div>
  </div>

  <h2 class="section">O que as três direções respeitam</h2>
  <ul class="principles">{principles}</ul>

  <nav class="nav" aria-label="Direções">{nav}</nav>
  {sections}

  <h2 class="section" id="comparar">Comparação</h2>
  <div class="tbl"><table class="compare"><thead><tr><th></th><th>A · Vigília</th><th>B · Vínculo</th><th>C · Assinatura</th></tr></thead><tbody>{cmp_rows}</tbody></table></div>

  <div class="rec">
    <p><b>Minha recomendação: A · Vigília.</b></p>
    <p>É a direção que traduz o nome de forma mais direta: vigiar como velar por alguém. Também é a que funciona melhor pequena, na tela inicial, e usa a fonte mais legível para quem enxerga pouco ou está com pressa. O escuro foi desenhado primeiro, porque é à noite que mais se precisa do app.</p>
    <p>Dá para combinar: o símbolo de A com a fonte de C, ou a paleta de B com o símbolo de A.</p>
  </div>
  <p class="answer">Responda com a letra (A, B ou C) e o que quiser ajustar. A direção escolhida é aplicada no código na V2.</p>

  <footer>Arquivos vetoriais de cada direção (símbolo, logo claro e escuro, ícone): <code>vgr-ai/docs/identidade-visual/v1/</code>. Briefing: <code>docs/identidade-visual/briefing.md</code>.</footer>
</div>'''

def main():
    os.makedirs(OUT, exist_ok=True)
    for key in 'ABC':
        d = os.path.join(OUT, SLUG[key]); os.makedirs(d, exist_ok=True)
        t = DIRECTIONS[key]['light']
        sym = symbol_svg(key, t['primary'], t['accentGraphic']).replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        open(os.path.join(d, 'simbolo.svg'), 'w').write(sym + '\n')
        open(os.path.join(d, 'logo-claro.svg'), 'w').write(logo_svg(key, 'light', True) + '\n')
        open(os.path.join(d, 'logo-escuro.svg'), 'w').write(logo_svg(key, 'dark', True) + '\n')
        open(os.path.join(d, 'icone.svg'), 'w').write(icon_svg(key, True) + '\n')
    open(os.path.join(OUT, 'index.html'), 'w').write(page() + '\n')
    print('written', OUT)

if __name__ == '__main__':
    main()
