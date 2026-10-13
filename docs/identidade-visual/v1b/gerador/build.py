"""Builds VGR identity V1b (round 24, decision 266): the consolidated
direction as vector files plus the presentation page.

Run from this folder: sh fetch_fonts.sh && python3 -B build.py
"""
import os
from glyphs import outline
from mark import (BOLD, symbol_svg, logo_horizontal, logo_vertical, icon_svg, themed_svg,
                  pattern_svg, write_files)
from tokens import TOKENS, MARK, PAIRS, MARK_PAIRS, BOARD_FIXES, SLOGAN, FONT, contrast

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)                       # docs/identidade-visual/v1b
FONT_STACK = "'Atkinson Hyperlegible Next', system-ui, sans-serif"

ROLE = {
    'bg': 'fundo', 'surface': 'cartão', 'text': 'texto', 'muted': 'texto secundário',
    'brand': 'marca', 'action': 'ação', 'accent': 'dourado (preenchimento)',
    'accentGraphic': 'dourado (gráfico)', 'accentText': 'dourado (texto)',
    'control': 'borda de controle', 'danger': 'pânico e erro', 'splash': 'abertura',
}

def fmt(r):
    return f'{r:.2f}'.replace('.', ',')

# ---------------------------------------------------------------- small icons
def ico(name, color='currentColor', w=2.2):
    paths = {
        'back': '<path d="M15 5l-7 7 7 7"/>',
        'plus': '<path d="M12 5v14M5 12h14"/>',
        'check': '<path d="M5 12.5l4.2 4.2L19 7"/>',
        'person': '<circle cx="12" cy="8" r="3.6"/><path d="M5 20c.8-3.6 3.6-5.4 7-5.4s6.2 1.8 7 5.4"/>',
        'chev': '<path d="M7 10l5 5 5-5"/>',
        'pin': '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0113 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
        'people': '<circle cx="8.5" cy="9" r="3"/><circle cx="16" cy="9.5" r="2.5"/><path d="M3 19c.6-3 2.8-4.6 5.5-4.6S13.4 16 14 19M14.5 14.6c2.6-.3 4.9 1 5.5 4.4"/>',
        'camera': '<rect x="3.5" y="7" width="17" height="12" rx="3"/><circle cx="12" cy="13" r="3.3"/><path d="M9 7l1.4-2.2h3.2L15 7"/>',
        'image': '<rect x="4" y="5" width="16" height="14" rx="3"/><path d="M4 16l4.5-4.5 4 4 2.5-2.5L20 18"/><circle cx="15.5" cy="9.5" r="1.5"/>',
        'search': '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.6-4.6"/>',
        'left': '<path d="M14 6l-6 6 6 6"/>', 'right': '<path d="M10 6l6 6-6 6"/>',
        'loc': '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/><circle cx="12" cy="12" r="7"/>',
    }[name]
    return (f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')

def mark_mini(mode):
    t = TOKENS[mode]
    return symbol_svg(t['brand'], t['accentGraphic'], 'mark', pad=1)

def sos():
    return '<span class="sos" aria-label="Botão de pânico">SOS</span>'

# ---------------------------------------------------------------- phone screens
def phone_vars(mode):
    return ';'.join(f'--{k}:{v}' for k, v in TOKENS[mode].items())

def cb(on):
    return f'<span class="cb{" on" if on else ""}">{ico("check", w=3) if on else ""}</span>'

def screen_splash(mode):
    word, ww, cap, _ = outline(BOLD, 'VGR', 30, 0.01)
    color = MARK['white'] if mode == 'light' else TOKENS['dark']['text']
    return (f'<div class="splash">{symbol_svg(MARK["white"] if mode == "light" else TOKENS["dark"]["brand"], MARK["gold"], "splash-mark")}'
            f'<svg class="splash-word" viewBox="0 {-cap - 1:.1f} {ww:.1f} {cap + 2:.1f}" role="img" aria-label="VGR">'
            f'<path d="{word}" fill="{color}"/></svg></div>')

def screen_feed(mode):
    items = [
        ('Roubo / furto · Criança', '~1 km · há 15 min', ''),
        ('Atividade suspeita · Veículo', '~2 km · há 40 min', '<span class="hint">Direção estimada: Leste</span>'),
        ('Desaparecimento · Adulto', '~4 km · hoje', '<span class="badge">Sua denúncia</span>'),
        ('Vandalismo · Propriedade', '~3 km · ontem', ''),
    ]
    rows = ''.join(f'<li class="card"><b>{a}</b><span class="mut">{b}</span>{c}</li>' for a, b, c in items)
    return (f'<div class="bar">{mark_mini(mode)}<span class="h">Por perto</span><span class="sp"></span>{sos()}'
            f'<span class="ib">{ico("person")}</span></div>'
            f'<div class="order"><span class="mut">Ordenar por</span><span class="seg"><span class="on">Mais recentes</span><span>Relevância</span></span></div>'
            f'<ul class="list">{rows}</ul>'
            f'<div class="fab" aria-label="Denunciar">{ico("plus", w=2.6)}</div>')

def screen_report(mode):
    def field(label, value):
        return f'<div class="lbl">{label}</div><div class="field"><span>{value}</span>{ico("chev")}</div>'
    return (f'<div class="bar">{ico("back")}<span class="h">Denunciar</span></div><div class="pad">'
            + field('O que aconteceu?', 'Atividade suspeita') + field('Quem ou o que está envolvido?', 'Veículo')
            + f'<div class="okrow">{ico("check", w=2.8)}<span>Localização capturada</span></div>'
            f'<div class="lbl">Fotos</div><div class="two"><span class="obtn">{ico("camera")}Câmera</span><span class="obtn">{ico("image")}Galeria</span></div>'
            f'<p class="tiny">Até 10 fotos. Elas sobem em segundo plano, e sua denúncia nunca espera.</p>'
            f'<div class="chk">{cb(True)}<span>Denunciar anonimamente</span></div>'
            f'<div class="btn">Enviar denúncia</div></div>')

def screen_offer(mode):
    types = [('Presença física', True), ('Repassar informação', False), ('Apoio remoto', False),
             ('Divulgar', True), ('Contribuição financeira', False)]
    rows = ''.join(f'<li>{cb(c)}<span>{n}</span></li>' for n, c in types)
    return (f'<div class="bar">{ico("back")}<span class="h">Oferecer ajuda</span></div>'
            f'<div class="pad"><div class="lbl">Como você quer ajudar?</div><ul class="checks">{rows}</ul>'
            f'<div class="card name"><div class="chk">{cb(False)}<b>Mostrar meu nome a quem denunciou</b></div>'
            f'<p>Na dúvida, deixe desmarcado: uma denúncia pode ser falsa, feita só para descobrir quem ajuda. '
            f'Sem o nome você continua podendo conversar, ser avaliado e receber recompensa.</p></div>'
            f'<div class="btn">Enviar oferta</div></div>')

def screen_panic(mode):
    return (f'<div class="bar">{ico("back")}<span class="h">Botão de pânico</span></div>'
            f'<div class="panic"><div class="panic-btn">Preciso de ajuda agora</div>'
            f'<p class="tiny">Isso notifica imediatamente os Respondentes Autorizados próximos com sua localização atual. '
            f'Use somente em uma emergência real.</p></div>')

SCREENS = [('splash', 'Abertura', screen_splash), ('feed', 'Por perto', screen_feed),
           ('report', 'Denunciar', screen_report), ('offer', 'Oferecer ajuda', screen_offer),
           ('panic', 'Pânico', screen_panic)]

def phone(mode, key, label, fn):
    cls = 'phone splash-bg' if key == 'splash' else 'phone'
    return (f'<figure class="phone-wrap"><div class="{cls}" style="{phone_vars(mode)}">'
            f'<div class="status"><span>9:41</span></div>{fn(mode)}</div>'
            f'<figcaption>{label}</figcaption></figure>')

def phones(mode):
    return ''.join(phone(mode, k, l, f) for k, l, f in SCREENS)

# ---------------------------------------------------------------- panel
def panel(mode):
    t = TOKENS[mode]
    word, ww, cap, _ = outline(BOLD, 'VGR', 20, 0.01)
    logo = (f'{symbol_svg(t["brand"], t["accentGraphic"], "pmark", pad=1)}'
            f'<svg class="pword" viewBox="0 {-cap - 1:.1f} {ww:.1f} {cap + 2:.1f}" role="img" aria-label="VGR">'
            f'<path d="{word}" fill="{t["brand"]}"/></svg><span class="mut">Painel</span>')
    col2 = ['Denúncias', 'Estatísticas de denúncias', 'Auditoria administrativa', 'Congelamento de Caso', 'Mediação de Recompensa']
    rows = [('Roubo / furto', 'Criança', 'Aberta', '13/10/2026 14:02'),
            ('Atividade suspeita', 'Veículo', 'Aberta', '13/10/2026 13:27'),
            ('Desaparecimento', 'Adulto', 'Resolvida', '12/10/2026 22:15'),
            ('Vandalismo', 'Propriedade', 'Aberta', '12/10/2026 19:40')]
    nav2 = ''.join(f'<span class="on">{n}</span>' if i == 0 else f'<span>{n}</span>' for i, n in enumerate(col2))
    trs = ''.join(f'<tr><td>{a}</td><td>{b}</td><td><span class="st{" done" if c == "Resolvida" else ""}">{c}</span></td>'
                  f'<td class="num">{d}</td></tr>' for a, b, c, d in rows)
    return (f'<div class="panel" style="{phone_vars(mode)}">'
            f'<div class="ptop">{logo}<span class="sp"></span><span class="ib">{ico("person")}</span></div>'
            f'<div class="pbody"><nav class="pcol1"><span class="on">Operações</span><span>Administração</span></nav>'
            f'<nav class="pcol2">{nav2}</nav>'
            f'<div class="pmain"><div class="ph">Denúncias</div>'
            f'<div class="psearch">{ico("search")}<span>Buscar por categoria ou assunto</span></div>'
            f'<table class="ptable"><thead><tr><th>Categoria</th><th>Assunto</th><th>Situação</th><th>Registrada em</th></tr></thead>'
            f'<tbody>{trs}</tbody></table>'
            f'<div class="ppager"><span class="mut">1–20 de 134</span><span class="pg">{ico("left")}</span><span class="pg">{ico("right")}</span></div>'
            f'</div></div></div>')

# ---------------------------------------------------------------- page pieces
def swatches(mode):
    t = TOKENS[mode]
    keys = ['bg', 'surface', 'text', 'muted', 'brand', 'action', 'accent', 'accentGraphic', 'accentText', 'control', 'danger', 'splash']
    return ''.join(f'<div class="sw"><span class="chip" style="background:{t[k]}"></span>'
                   f'<span class="role">{ROLE[k]}</span><code>{t[k]}</code></div>' for k in keys)

def contrast_table(mode):
    t = TOKENS[mode]
    rows = []
    for fg, bg, minimum, label in PAIRS:
        r = contrast(t[fg], t[bg])
        ok = r >= minimum
        rows.append(f'<tr><td><span class="pair" style="background:{t[bg]};color:{t[fg]};border-color:{t["divider"]}">Aa</span></td>'
                    f'<td>{label}</td><td class="num">{fmt(r)}:1</td><td class="num">{minimum:g}:1</td>'
                    f'<td class="{"pass" if ok else "fail"}">{"passa" if ok else "falha"}</td></tr>')
    return ('<div class="tbl"><table class="ctab"><thead><tr><th></th><th>Par</th><th>Medido</th><th>Piso</th><th></th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')

def mark_table():
    rows = ''.join(f'<tr><td>{label}</td><td class="num">{fmt(contrast(MARK[fg], MARK[bg]))}:1</td><td class="num">{m:g}:1</td></tr>'
                   for fg, bg, m, label in MARK_PAIRS)
    return f'<table class="ctab small-t"><tbody>{rows}</tbody></table>'

def fixes():
    rows = []
    for role, before, after, why in BOARD_FIXES:
        b = f'<span class="dot" style="background:{before}"></span><code>{before}</code>'
        a = (f'<span class="dot" style="background:{after}"></span><code>{after}</code>' if after.startswith('#')
             else '<span class="mut-t">sai</span>')
        rows.append(f'<tr><th scope="row">{role}</th><td class="nowrap">{b}</td><td class="nowrap">{a}</td><td>{why}</td></tr>')
    return ('<div class="tbl"><table class="fix"><thead><tr><th>Onde</th><th>Na prancha</th><th>Agora</th><th>Por quê</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')

CHANGES = [
    ('Troféu e "Você ganhou +10 pontos"', 'Sem troféu e sem pontos. O dourado aparece no selo "Recompensa garantida".', '262'),
    ('Aba "Recompensas" na barra inferior', 'Não existe. O app abre em "Por perto", como hoje.', '262'),
    ('Escudo com check', 'O arco do símbolo é o sinal de proteção.', '263'),
    ('"Olá, Ana" com foto', 'O título da tela. Nenhum rosto ou nome na tela inicial.', '264'),
    ('"Você está em uma área segura"', 'Removido: o app não avalia a segurança de uma área.', '264'),
    ('Ponto de ônibus, cartões, garrafa, sacola', 'Ficam para a rodada de divulgação.', '265'),
    ('Telas ilustrativas (Pedir ajuda, Informação, Mapa)', 'As telas reais do app, com os textos de hoje.', '261'),
]

MAP = [
    ('Símbolo', 'Um arco que cobre um ponto aceso: velar por alguém. É também o sinal de proteção.', '250, 252, 261, 263'),
    ('Azul-marinho', 'Confiança e calma. É a noite em que a vigília acontece.', '253, 261'),
    ('Verde-petróleo', 'A cor de agir: denunciar, oferecer ajuda, enviar. Ação sem alarme.', '2, 253, 261'),
    ('Dourado', 'A luz acesa do símbolo. Como recompensa, só no selo, e com parcimônia.', '1, 30, 101, 262'),
    ('Vermelho', 'Só pânico e erro.', '51, 253'),
    ('Atkinson Hyperlegible Next', 'Feita para baixa visão. Vai embutida no app.', '255, 257'),
    ('Ícone', 'Forma abstrata e a sigla: não diz "denúncia" na tela inicial.', '238, 252'),
    ('Telas', 'Sem foto, nome ou promessa de segurança. Nome desmarcado por padrão ao oferecer ajuda.', '6, 41, 237, 238, 264'),
    ('Modo escuro', 'Desenhado junto, com abertura escura para chamar menos atenção à noite.', '256'),
    ('Slogan', '"Pessoas cuidando de pessoas": o vínculo entre quem denuncia e quem ajuda.', 'obj. 4, 2, 261'),
]

def home_screen(dark):
    def other(label, glyph):
        return f'<div class="app"><span class="gen">{glyph}</span><span>{label}</span></div>'
    cal = '<svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="15" rx="3" fill="none" stroke="#fff" stroke-width="2"/><path d="M4 10h16M9 3v4M15 3v4" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>'
    notes = '<svg viewBox="0 0 24 24"><path d="M7 8h10M7 12h10M7 16h6" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>'
    sun = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="5" fill="none" stroke="#fff" stroke-width="2"/></svg>'
    return (f'<div class="home{" night" if dark else ""}">{other("Agenda", cal)}{other("Notas", notes)}'
            f'<div class="app">{icon_svg("square", uid="home" + ("d" if dark else "l"))}<span>VGR</span></div>{other("Clima", sun)}</div>')

CSS = """
/* Layout: a brand book in one column. The page wears the identity itself: its tokens, its font. Specimens keep their own fixed colors. */
:root {
  --bg:#F4F6F8; --surface:#FFFFFF; --ink:#131D33; --soft:#627289; --line:#DDE2EA; --brand:#203B70; --action:#1B7168; --gold:#BB8329;
  --display:'Atkinson Hyperlegible Next', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --mono:'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#0A1120; --surface:#111A2D; --ink:#E9EDF6; --soft:#A9B3C9; --line:#243049; --brand:#93B6FF; --action:#5CCDBB; --gold:#D8A34D; color-scheme:dark; } }
:root[data-theme="dark"] { --bg:#0A1120; --surface:#111A2D; --ink:#E9EDF6; --soft:#A9B3C9; --line:#243049; --brand:#93B6FF; --action:#5CCDBB; --gold:#D8A34D; color-scheme:dark; }
body { background:var(--bg); color:var(--ink); font-family:var(--display); font-size:16px; line-height:1.55; }
.wrap { max-width:1180px; margin:0 auto; padding-inline:20px; padding-block:36px 72px; }
a { color:var(--brand); }
:focus-visible { outline:2px solid var(--brand); outline-offset:3px; border-radius:6px; }
.eyebrow { font-family:var(--mono); font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--soft); margin:0; }
h1 { font-size:clamp(32px,5.4vw,52px); line-height:1.05; font-weight:800; letter-spacing:-.015em; margin:.3em 0 .35em; text-wrap:balance; }
.lede { max-width:66ch; font-size:18px; color:var(--soft); margin:0; }
.lede b { color:var(--ink); }
.hero { display:grid; grid-template-columns:minmax(0,1.35fr) minmax(0,1fr); gap:14px; margin-top:28px; }
.hero .stage { border-radius:20px; display:flex; flex-direction:column; justify-content:center; gap:22px; padding:44px 40px; min-height:260px; }
.hero .stage .logo { width:min(100%,460px); height:auto; }
.hero .slogan { font-size:clamp(19px,2.3vw,24px); line-height:1.3; margin:0; max-width:24ch; }
.stage.light { background:#FFFFFF; border:1px solid var(--line); }
.stage.light .slogan { color:#627289; }
.stage.dark { background:#0A1120; border:1px solid var(--line); }
.stage.dark .slogan { color:#A9B3C9; }
section { margin-top:64px; }
.shead { display:flex; align-items:baseline; gap:14px; flex-wrap:wrap; border-top:2px solid var(--ink); padding-top:14px; margin-bottom:18px; }
.shead h2 { font-size:28px; line-height:1.15; margin:0; font-weight:800; }
.shead .refs { margin-left:auto; }
.intro { max-width:68ch; margin:0 0 18px; }
.refs { font-family:var(--mono); font-size:12px; color:var(--soft); white-space:nowrap; }
.grid { display:grid; gap:14px; grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr)); }
.tile { border-radius:16px; border:1px solid var(--line); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px; padding:30px 22px 14px; min-height:200px; }
.tile .logo { width:min(100%,330px); height:auto; }
.tile .logo.v { width:min(100%,190px); }
.tile .cap { font-size:13px; align-self:flex-start; margin-top:auto; }
.t-white { background:#FFFFFF; } .t-white .cap { color:#627289; }
.t-night { background:#0A1120; } .t-night .cap { color:#A9B3C9; }
.t-navy { background:#203B70; } .t-navy .cap { color:#D5DEEE; }
.t-mono { background:#FFFFFF; color:#131D33; } .t-mono .cap { color:#627289; }
.block { background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:18px; min-width:0; }
.block h3 { font-size:13px; letter-spacing:.06em; text-transform:uppercase; color:var(--soft); margin:0 0 12px; font-weight:700; }
.note { font-size:14px; color:var(--soft); margin:12px 0 0; }
.icons { display:flex; gap:18px; align-items:flex-end; flex-wrap:wrap; }
.icons figure { margin:0; display:flex; flex-direction:column; align-items:center; gap:6px; font-size:12px; color:var(--soft); }
.icons .appicon, .icons .themed { width:92px; height:92px; display:block; }
.themed-bg { background:#DCE6F7; border-radius:50%; width:92px; height:92px; display:flex; }
.themed-bg svg { width:92px; height:92px; }
.tab { display:flex; align-items:center; gap:8px; background:var(--bg); border:1px solid var(--line); border-radius:10px 10px 0 0; padding:8px 12px; width:max-content; max-width:100%; font-size:13px; }
.tab svg { width:16px; height:16px; flex:none; }
.fav-sizes { display:flex; gap:12px; align-items:flex-end; margin-top:12px; }
.fav-sizes svg { display:block; }
.home { background:linear-gradient(160deg,#7C93B8,#4A5F82); border-radius:16px; padding:18px 10px 14px; display:grid; grid-template-columns:repeat(4,1fr); gap:8px; }
.home.night { background:linear-gradient(160deg,#1A2233,#0B0F18); }
.app { display:flex; flex-direction:column; align-items:center; gap:6px; color:#FFFFFF; font-size:11.5px; min-width:0; }
.app .appicon, .gen { width:50px; height:50px; border-radius:12px; display:block; }
.gen { background:#5B6878; display:flex; align-items:center; justify-content:center; }
.gen svg { width:24px; height:24px; }
.sws { display:grid; grid-template-columns:repeat(auto-fill,minmax(112px,1fr)); gap:10px 8px; }
.sw { display:flex; flex-direction:column; gap:3px; font-size:12.5px; min-width:0; }
.sw .chip { height:40px; border-radius:10px; border:1px solid var(--line); }
.sw .role { color:var(--soft); line-height:1.25; }
code, .num { font-family:var(--mono); font-size:12px; font-variant-numeric:tabular-nums; }
.tbl { overflow-x:auto; }
table { border-collapse:collapse; width:100%; font-size:14px; }
th, td { text-align:left; padding:7px 8px; border-bottom:1px solid var(--line); vertical-align:middle; }
thead th { color:var(--soft); font-weight:700; font-size:13px; }
.pair { display:inline-block; padding:2px 8px; border-radius:6px; font-weight:700; border:1px solid; }
.pass { color:var(--action); font-weight:700; }
.fail { color:#D23535; font-weight:700; }
.small-t td { font-size:13px; }
.fix .dot, .dot { display:inline-block; width:14px; height:14px; border-radius:50%; vertical-align:-2px; margin-right:6px; border:1px solid var(--line); }
.nowrap { white-space:nowrap; }
.mut-t { color:var(--soft); }
.type { display:grid; gap:14px; grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr)); }
.weights { display:flex; flex-direction:column; gap:6px; font-size:26px; line-height:1.2; }
.weights span small { font-size:13px; color:var(--soft); font-family:var(--mono); margin-left:8px; }
.glyphs { display:flex; gap:22px; flex-wrap:wrap; font-size:46px; line-height:1; font-weight:700; }
.glyphs span { display:flex; flex-direction:column; align-items:center; gap:6px; }
.glyphs small { font-size:12px; font-weight:400; color:var(--soft); font-family:var(--mono); }
.sample-t { font-size:15px; max-width:52ch; }
.elements { display:grid; gap:14px; grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr)); }
.el { display:flex; flex-direction:column; align-items:flex-start; gap:10px; }
.el .glyph { width:44px; height:44px; color:var(--brand); }
.el .glyph svg { width:44px; height:44px; display:block; }
.el .glyph circle { fill:var(--gold); }
.el b { font-size:16px; }
.el p { margin:0; font-size:14px; color:var(--soft); }
.seal { display:inline-flex; align-items:center; gap:7px; background:#D8A34D; color:#131D33; font-weight:700; font-size:14px; border-radius:999px; padding:5px 12px 5px 9px; }
.seal i { width:9px; height:9px; border-radius:50%; background:#131D33; display:block; }
.pattern { width:100%; height:auto; display:block; }
.pat-light { background:#FFFFFF; } .pat-light h3 { color:#627289; }
.pat-dark { background:#0A1120; } .pat-dark h3 { color:#A9B3C9; }
.phones { display:grid; gap:16px; grid-template-columns:repeat(auto-fill,minmax(210px,1fr)); justify-items:center; }
.mode-label { font-size:13px; letter-spacing:.06em; text-transform:uppercase; color:var(--soft); font-weight:700; margin:22px 0 10px; }
.phone-wrap { margin:0; display:flex; flex-direction:column; gap:6px; align-items:center; }
.phone-wrap figcaption { font-size:13px; color:var(--soft); }
.phone { width:210px; height:440px; border-radius:28px; border:6px solid #0C0D10; background:var(--bg); color:var(--text);
  font-family:var(--display); font-size:12.5px; line-height:1.4; position:relative; overflow:hidden; display:flex; flex-direction:column; }
.phone.splash-bg { background:var(--splash); }
.phone .status { height:22px; padding:5px 16px 0; font-size:10.5px; font-weight:700; color:var(--text); }
.phone.splash-bg .status { color:#FFFFFF; }
.phone .bar { display:flex; align-items:center; gap:8px; padding:6px 12px 10px; color:var(--text); }
.phone .bar > svg { width:20px; height:20px; flex:none; }
.phone .bar .mark { width:26px; height:auto; flex:none; }
.phone .h { font-size:17px; font-weight:700; }
.phone .sp { flex:1; }
.phone .ib { width:20px; height:20px; color:var(--text); display:flex; }
.phone .ib svg { width:20px; height:20px; }
.phone .sos { font-size:10px; font-weight:800; color:var(--danger); border:2px solid var(--danger); border-radius:6px; padding:0 3px; letter-spacing:.02em; }
.phone .order { display:flex; flex-direction:column; align-items:flex-start; gap:3px; padding:0 12px 8px; font-size:11px; }
.phone .seg { display:flex; border:1px solid var(--control); border-radius:999px; overflow:hidden; }
.phone .seg span { padding:2px 9px; color:var(--text); white-space:nowrap; }
.phone .seg .on { background:var(--brand); color:var(--onBrand); font-weight:700; }
.phone .list { list-style:none; margin:0; padding:0 10px; display:flex; flex-direction:column; gap:7px; }
.phone .card { background:var(--surface); border:1px solid var(--divider); border-radius:14px; padding:8px 11px; display:flex; flex-direction:column; gap:1px; align-items:flex-start; }
.phone .mut { color:var(--muted); font-size:11.5px; }
.phone .hint { color:var(--muted); font-size:11px; }
.phone .badge { margin-top:3px; font-size:10.5px; font-weight:700; color:var(--brand); border:1px solid var(--brand); border-radius:999px; padding:0 7px; }
.phone .fab { position:absolute; right:14px; bottom:16px; width:50px; height:50px; border-radius:16px; background:var(--action); color:var(--onAction); display:flex; align-items:center; justify-content:center; }
.phone .fab svg { width:24px; height:24px; }
.phone .pad { padding:0 12px; display:flex; flex-direction:column; gap:6px; }
.phone .lbl { font-size:11.5px; font-weight:700; color:var(--muted); margin-top:4px; }
.phone .field { display:flex; align-items:center; justify-content:space-between; border:1.5px solid var(--control); border-radius:12px; padding:7px 10px; background:var(--surface); }
.phone .field svg { width:16px; height:16px; color:var(--muted); }
.phone .okrow { display:flex; gap:6px; align-items:center; color:var(--action); font-weight:700; font-size:12px; margin-top:4px; }
.phone .okrow svg { width:16px; height:16px; }
.phone .two { display:flex; gap:6px; }
.phone .obtn { flex:1; display:flex; align-items:center; justify-content:center; gap:5px; border:1.5px solid var(--control); border-radius:12px; padding:6px; font-weight:700; color:var(--brand); }
.phone .obtn svg { width:16px; height:16px; }
.phone .tiny { margin:0; font-size:10.5px; color:var(--muted); line-height:1.4; }
.phone .chk { display:flex; gap:8px; align-items:center; }
.phone .cb { width:19px; height:19px; border-radius:6px; border:2px solid var(--control); display:flex; align-items:center; justify-content:center; flex:none; color:var(--onAction); }
.phone .cb.on { background:var(--action); border-color:var(--action); }
.phone .cb svg { width:13px; height:13px; }
.phone .checks { list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:6px; }
.phone .checks li { display:flex; gap:8px; align-items:center; }
.phone .name { gap:5px; margin-top:4px; }
.phone .name p { margin:0; font-size:10.5px; color:var(--muted); line-height:1.4; }
.phone .btn { margin-top:6px; background:var(--action); color:var(--onAction); border-radius:14px; text-align:center; padding:10px; font-weight:700; }
.phone .panic { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:18px; padding:0 18px 40px; text-align:center; }
.phone .panic-btn { width:150px; height:150px; border-radius:50%; background:var(--danger); color:var(--onDanger); display:flex; align-items:center; justify-content:center; text-align:center; font-weight:800; font-size:16px; line-height:1.25; padding:20px; }
.phone .splash { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; position:relative; }
.phone .splash-mark { width:96px; height:auto; margin-bottom:30px; }
.phone .splash-word { position:absolute; bottom:34px; width:44px; height:auto; }
.panels { display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr)); }
.panel-wrap { overflow-x:auto; border-radius:14px; }
.panel { min-width:520px; min-height:330px; border-radius:14px; border:1px solid var(--line); overflow:hidden; background:var(--bg); color:var(--text); font-family:var(--display); font-size:12px; display:flex; flex-direction:column; }
.panel .ptop { display:flex; align-items:center; gap:7px; padding:8px 12px; background:var(--surface); border-bottom:1px solid var(--divider); }
.panel .pmark { width:22px; height:auto; }
.panel .pword { width:30px; height:auto; }
.panel .mut { color:var(--muted); }
.panel .sp { flex:1; }
.panel .ib { width:18px; height:18px; color:var(--muted); display:flex; }
.panel .ib svg { width:18px; height:18px; }
.panel .pbody { flex:1; display:flex; min-height:0; }
.panel nav { display:flex; flex-direction:column; padding:6px 0; }
.panel nav span { padding:6px 12px; color:var(--text); }
.panel .pcol1 { width:96px; background:var(--navStrong); }
.panel .pcol2 { width:150px; background:var(--navSoft); border-right:1px solid var(--divider); }
.panel nav .on { font-weight:700; color:var(--brand); box-shadow:inset 3px 0 0 var(--brand); }
.panel .pmain { flex:1; padding:10px 14px; display:flex; flex-direction:column; gap:8px; min-width:0; }
.panel .ph { font-size:16px; font-weight:700; }
.panel .psearch { display:flex; gap:6px; align-items:center; border:1px solid var(--control); border-radius:10px; padding:4px 8px; color:var(--muted); background:var(--surface); }
.panel .psearch svg { width:14px; height:14px; }
.panel .ptable { font-size:11px; background:var(--surface); border-radius:8px; }
.panel .ptable th, .panel .ptable td { padding:5px 7px; border-bottom:1px solid var(--divider); color:var(--text); }
.panel .ptable th { color:var(--muted); font-size:10.5px; }
.panel .num { font-size:10.5px; white-space:nowrap; }
.panel .st { border:1px solid var(--brand); color:var(--brand); border-radius:999px; padding:0 6px; font-size:10px; font-weight:700; }
.panel .st.done { border-color:var(--control); color:var(--muted); }
.panel .ppager { display:flex; justify-content:flex-end; align-items:center; gap:6px; margin-top:auto; }
.panel .pg { width:22px; height:22px; border:1px solid var(--control); border-radius:7px; display:flex; align-items:center; justify-content:center; color:var(--text); }
.panel .pg svg { width:13px; height:13px; }
.changes th[scope=row], .map th[scope=row] { font-weight:700; }
.changes td.dec, .map td.dec { font-family:var(--mono); font-size:12px; color:var(--soft); white-space:nowrap; }
.next { background:var(--surface); border:1px solid var(--line); border-radius:18px; padding:22px 24px; display:grid; gap:10px; max-width:78ch; }
.next h2 { margin:0; font-size:24px; font-weight:800; }
.next p { margin:0; }
.next ul { margin:0; padding-left:20px; display:flex; flex-direction:column; gap:4px; }
footer { margin-top:40px; font-size:14px; color:var(--soft); max-width:78ch; }
@media (max-width:760px) { .hero { grid-template-columns:1fr; } .hero .stage { padding:30px 22px; } }
@media (max-width:520px) { .home { gap:4px; } .shead .refs { margin-left:0; } }
@media (prefers-reduced-motion: reduce) { * { scroll-behavior:auto !important; } }
"""

def page():
    lt, dk = TOKENS['light'], TOKENS['dark']
    changes = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td class="dec">{c}</td></tr>' for a, b, c in CHANGES)
    maprows = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td class="dec">{c}</td></tr>' for a, b, c in MAP)
    pin, people = ico('pin', w=2), ico('people', w=2)
    fav_tab = icon_svg('favicon', cls='', uid='tab')
    fav32 = icon_svg('favicon', cls='', uid='f32').replace('<svg ', '<svg width="32" height="32" ', 1)
    fav16 = icon_svg('favicon', cls='', uid='f16').replace('<svg ', '<svg width="16" height="16" ', 1)
    return f'''<title>Identidade VGR</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <p class="eyebrow">Rodada 24 · V1b · decisões 261–266</p>
  <h1>A identidade do VGR, consolidada</h1>
  <p class="lede">A sua prancha, com o que as decisões 261 a 264 pedem: <b>cores que passam no AA, modo escuro, logo em vetor e as telas reais do app.</b> Se estiver de acordo, a V2 leva isto para o código.</p>

  <div class="hero">
    <div class="stage light">{logo_horizontal('claro')}<p class="slogan">{SLOGAN}</p></div>
    <div class="stage dark">{logo_horizontal('escuro')}<p class="slogan">{SLOGAN}</p></div>
  </div>

  <section aria-labelledby="s-logo">
    <div class="shead"><h2 id="s-logo">Logo</h2><span class="refs">250 · 261</span></div>
    <p class="intro">O símbolo, as letras e o descritor em vetor. "VGR" é a Atkinson Hyperlegible Next ExtraBold convertida em contorno, e o descritor tem a largura exata da palavra. No claro, o ponto usa o dourado mais escuro, que passa 3:1 sobre o branco.</p>
    <div class="grid">
      <div class="tile t-white">{logo_horizontal('claro')}<span class="cap">Horizontal · claro</span></div>
      <div class="tile t-night">{logo_horizontal('escuro')}<span class="cap">Horizontal · escuro</span></div>
      <div class="tile t-navy">{logo_horizontal('negativo')}<span class="cap">Negativo, sobre o azul da marca</span></div>
      <div class="tile t-white">{logo_vertical('claro', cls='logo v')}<span class="cap">Vertical · claro</span></div>
      <div class="tile t-navy">{logo_vertical('negativo', cls='logo v')}<span class="cap">Vertical · negativo</span></div>
      <div class="tile t-mono">{logo_horizontal('mono')}<span class="cap">Uma cor só (carimbo, gravação, documentos)</span></div>
    </div>
  </section>

  <section aria-labelledby="s-icon">
    <div class="shead"><h2 id="s-icon">Ícone do app</h2><span class="refs">238 · 252 · 261</span></div>
    <p class="intro">Um ícone só, no azul da marca, com o arco branco e o ponto dourado (4,82:1 sobre o azul). A variação verde saiu. Na tela inicial aparecem só o símbolo e "VGR".</p>
    <div class="grid">
      <div class="block"><h3>Nas máscaras</h3>
        <div class="icons">
          <figure>{icon_svg('square', uid='sq')}<figcaption>iPhone</figcaption></figure>
          <figure>{icon_svg('circle', uid='ci')}<figcaption>Android</figcaption></figure>
          <figure><span class="themed-bg">{themed_svg('#1F2F55', cls='themed')}</span><figcaption>Android temático</figcaption></figure>
        </div>
        <p class="note">No Android o símbolo fica dentro da área segura do ícone adaptativo. O ícone temático (Android 13 em diante) usa uma cor só, que o sistema tinge.</p></div>
      <div class="block"><h3>Na tela inicial</h3>{home_screen(False)}<div style="height:10px"></div>{home_screen(True)}
        <p class="note">Ao lado de outros apps, de dia e à noite. Nada nele diz "denúncia".</p></div>
      <div class="block"><h3>Favicon do painel e da web</h3>
        <div class="tab">{fav_tab.replace('<svg ', '<svg width="16" height="16" ', 1)}<span>VGR · Painel</span></div>
        <div class="fav-sizes">{fav32}{fav16}</div>
        <p class="note">Em 32 e 16 pixels o símbolo ocupa mais do quadro, para continuar legível.</p></div>
    </div>
  </section>

  <section aria-labelledby="s-color">
    <div class="shead"><h2 id="s-color">Cores</h2><span class="refs">256 · 257 · 261</span></div>
    <p class="intro">As cores da prancha, divididas por papel. O claro e o escuro foram desenhados juntos. Cada par de texto e de gráfico foi calculado contra o piso da decisão 257.</p>
    <div class="grid">
      <div class="block"><h3>Claro</h3><div class="sws">{swatches('light')}</div></div>
      <div class="block"><h3>Escuro</h3><div class="sws">{swatches('dark')}</div></div>
    </div>
    <div class="grid" style="margin-top:14px">
      <div class="block"><h3>Contraste · claro</h3>{contrast_table('light')}</div>
      <div class="block"><h3>Contraste · escuro</h3>{contrast_table('dark')}</div>
    </div>
    <div class="grid" style="margin-top:14px">
      <div class="block"><h3>O que mudou nas cores da prancha</h3>{fixes()}</div>
      <div class="block"><h3>Ícone</h3>{mark_table()}<p class="note">Os {len(PAIRS) * 2 + len(MARK_PAIRS)} pares passam. O dourado da prancha continua como preenchimento e sobre o azul; o tom mais escuro só entra onde o dourado é desenho sobre fundo claro.</p></div>
    </div>
  </section>

  <section aria-labelledby="s-type">
    <div class="shead"><h2 id="s-type">Fonte</h2><span class="refs">255 · 257</span></div>
    <p class="intro">Atkinson Hyperlegible Next, do Braille Institute, feita para quem enxerga pouco. Licença OFL. Vai embutida no app e nunca é baixada durante o uso.</p>
    <div class="type">
      <div class="block"><h3>Pesos</h3><div class="weights">
        <span style="font-weight:400">Quem está perto pode ajudar<small>400</small></span>
        <span style="font-weight:600">Quem está perto pode ajudar<small>600</small></span>
        <span style="font-weight:700">Quem está perto pode ajudar<small>700</small></span>
        <span style="font-weight:800">VGR<small>800, só no logo</small></span></div></div>
      <div class="block"><h3>Letras que não se confundem</h3>
        <div class="glyphs"><span>Il1<small>i, L, um</small></span><span>O0<small>o, zero</small></span><span>rn m<small>r+n, m</small></span><span>B8<small>B, oito</small></span></div>
        <p class="note sample-t">É isso que a torna boa com pouca luz, com pressa ou com a tela pequena: "~1 km · há 15 min" não vira outra coisa.</p></div>
    </div>
  </section>

  <section aria-labelledby="s-el">
    <div class="shead"><h2 id="s-el">Elementos</h2><span class="refs">101 · 262 · 263</span></div>
    <div class="elements">
      <div class="block el"><span class="glyph">{pin}</span><b>Denunciar</b><p>O lugar onde aconteceu. Perto importa.</p></div>
      <div class="block el"><span class="glyph">{people}</span><b>Ajuda próxima</b><p>Pessoas que se aproximam para ajudar.</p></div>
      <div class="block el"><span class="seal"><i></i>Recompensa garantida</span><b>Selo de recompensa</b><p>O único lugar onde a recompensa aparece, no dourado do ponto (262). Entra no app quando a recompensa em dinheiro for ligada; na fase fechada ela está desligada (247).</p></div>
      <div class="block el"><span class="glyph">{symbol_svg('currentColor', '#BB8329', '')}</span><b>Proteção</b><p>O próprio símbolo, no lugar do escudo (263).</p></div>
    </div>
    <div class="grid" style="margin-top:14px">
      <div class="block pat-light"><h3>Padrão de arcos · claro</h3>{pattern_svg('#E6EAF1', MARK['navy'], MARK['gold'], uid='pl')}</div>
      <div class="block pat-dark"><h3>Padrão de arcos · escuro</h3>{pattern_svg('#18233A', '#93B6FF', MARK['gold'], uid='pd')}</div>
    </div>
    <p class="note">O padrão é para material da loja e de divulgação (V3). Dentro do app as telas ficam limpas.</p>
  </section>

  <section aria-labelledby="s-app">
    <div class="shead"><h2 id="s-app">Telas reais do app</h2><span class="refs">237 · 256 · 264</span></div>
    <p class="intro">Os textos são os do app de hoje. O verde-petróleo é a cor de agir (denunciar, enviar), o azul marca seleção e identidade, e o vermelho só aparece no pânico. A abertura é escura no modo escuro, para chamar menos atenção à noite.</p>
    <p class="mode-label">Claro</p><div class="phones">{phones('light')}</div>
    <p class="mode-label">Escuro</p><div class="phones">{phones('dark')}</div>
  </section>

  <section aria-labelledby="s-panel">
    <div class="shead"><h2 id="s-panel">Painel, versão sóbria</h2><span class="refs">215 · 258</span></div>
    <p class="intro">As mesmas cores e a mesma fonte, sem padrão nem ilustração. As duas colunas de navegação ganham tons do azul da marca, e o dourado fica só no ponto do logo.</p>
    <div class="panels"><div class="panel-wrap">{panel('light')}</div><div class="panel-wrap">{panel('dark')}</div></div>
  </section>

  <section aria-labelledby="s-changes">
    <div class="shead"><h2 id="s-changes">O que mudou da sua prancha</h2><span class="refs">261–265</span></div>
    <div class="tbl"><table class="changes"><thead><tr><th>Na prancha</th><th>Agora</th><th>Decisão</th></tr></thead><tbody>{changes}</tbody></table></div>
  </section>

  <section aria-labelledby="s-map">
    <div class="shead"><h2 id="s-map">O que cada elemento representa</h2><span class="refs">251</span></div>
    <div class="tbl"><table class="map"><thead><tr><th>Elemento</th><th>O que diz</th><th>Decisões</th></tr></thead><tbody>{maprows}</tbody></table></div>
  </section>

  <section aria-labelledby="s-next">
    <div class="next">
      <h2 id="s-next">Próximo passo: V2</h2>
      <p>Com a sua aprovação e um "pode seguir", a V2 aplica esta identidade nos dois apps:</p>
      <ul>
        <li>cores e fonte no <code>vgr_widgets</code>, que vestem todas as telas de uma vez;</li>
        <li>ícones do Android (adaptativo e temático), do iPhone e o favicon;</li>
        <li>tela de abertura, clara e escura;</li>
        <li>nome "VGR" no aparelho e na web;</li>
        <li>o painel na versão sóbria;</li>
        <li>conferência no navegador, no claro e no escuro.</li>
      </ul>
    </div>
  </section>

  <footer>Arquivos em vetor: <code>vgr-ai/docs/identidade-visual/v1b/svg/</code>. Cores: <code>v1b/gerador/tokens.py</code>, que a V2 leva para o código. Sua prancha: <code>v1b/prancha-valdo.webp</code>. As três direções da V1 continuam em <code>v1/</code>.</footer>
</div>'''

def main():
    files = write_files(os.path.join(OUT, 'svg'))
    with open(os.path.join(OUT, 'index.html'), 'w') as fh:
        fh.write(page() + '\n')
    print('written', OUT, files)

if __name__ == '__main__':
    main()
