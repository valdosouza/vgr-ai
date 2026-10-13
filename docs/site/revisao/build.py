"""Review page for the site texts (round 25, S1).

Reads ../textos/{pt,en}/*.md and writes index.html: every page side by
side in Portuguese and English, with the decisions each paragraph comes
from and the fields still to fill highlighted. Run: python3 -B build.py
"""
import html, os, re
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'textos')
LANGS = ('pt', 'en')

REF = re.compile(r'\s*<!--\s*([0-9][0-9 ,–\-a-z.]*)\s*-->\s*$')
FIELD = re.compile(r'\[\[([A-Z_]+)\]\]')

def read(lang):
    pages = []
    for name in sorted(os.listdir(os.path.join(SRC, lang))):
        if not name.endswith('.md'):
            continue
        text = open(os.path.join(SRC, lang, name), encoding='utf-8').read()
        _, front, body = text.split('---', 2)
        meta = yaml.safe_load(front)
        meta['file'] = name
        meta['body'] = body.strip('\n')
        pages.append(meta)
    return sorted(pages, key=lambda p: p['order'])

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = FIELD.sub(r'<mark class="field">\1</mark>', s)
    return s

def split_ref(line):
    m = REF.search(line)
    if not m:
        return line, ''
    return line[:m.start()], f'<span class="ref" title="Decisões">{html.escape(m.group(1).strip())}</span>'

def render(md):
    """The Markdown subset the texts use: ##/###, paragraphs, - lists."""
    out, para, items = [], [], []

    def flush_para():
        if para:
            text, ref = split_ref(' '.join(para))
            out.append(f'<p>{inline(text)}{ref}</p>')
            para.clear()

    def flush_list():
        if items:
            out.append('<ul>' + ''.join(f'<li>{inline(t)}{r}</li>' for t, r in items) + '</ul>')
            items.clear()

    for raw in md.split('\n'):
        line = raw.rstrip()
        if not line.strip():
            flush_para(); flush_list()
        elif line.startswith('### '):
            flush_para(); flush_list()
            out.append(f'<h4>{inline(line[4:])}</h4>')
        elif line.startswith('## '):
            flush_para(); flush_list()
            out.append(f'<h3>{inline(line[3:])}</h3>')
        elif line.startswith('- '):
            flush_para()
            items.append(split_ref(line[2:]))
        elif line.startswith('  ') and items:
            text, ref = items[-1]
            more, ref2 = split_ref(line.strip())
            items[-1] = (text + ' ' + more, ref2 or ref)
        else:
            flush_list()
            para.append(line.strip())
    flush_para(); flush_list()
    return '\n'.join(out)

CSS = """
/* Layout: a reading desk — page list on the left, the two languages side by side. Light/dark from the VGR tokens. */
:root {
  --bg:#F4F6F8; --surface:#FFFFFF; --ink:#131D33; --soft:#627289; --line:#DDE2EA; --brand:#203B70; --action:#1B7168;
  --field-bg:#FBEFD9; --field-ink:#6B4A12; --legal-bg:#E8EEF8;
  --font:'Atkinson Hyperlegible Next', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --mono:'Atkinson Hyperlegible Mono', ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#0A1120; --surface:#111A2D; --ink:#E9EDF6; --soft:#A9B3C9; --line:#243049; --brand:#93B6FF; --action:#5CCDBB; --field-bg:#4A3A17; --field-ink:#F6E3BF; --legal-bg:#18233A; color-scheme:dark; } }
:root[data-theme="dark"] { --bg:#0A1120; --surface:#111A2D; --ink:#E9EDF6; --soft:#A9B3C9; --line:#243049; --brand:#93B6FF; --action:#5CCDBB; --field-bg:#4A3A17; --field-ink:#F6E3BF; --legal-bg:#18233A; color-scheme:dark; }
body { background:var(--bg); color:var(--ink); font-family:var(--font); font-size:16px; line-height:1.6; }
.wrap { max-width:1320px; margin:0 auto; padding-inline:20px; padding-block:28px 64px; }
.eyebrow { font-family:var(--mono); font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--soft); margin:0; }
h1 { font-size:clamp(28px,4.4vw,42px); line-height:1.08; font-weight:800; margin:.25em 0 .4em; text-wrap:balance; }
.lede { max-width:72ch; color:var(--soft); margin:0 0 6px; }
.lede b { color:var(--ink); }
.notes { display:grid; gap:12px; grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr)); margin:22px 0 8px; }
.note { background:var(--surface); border:1px solid var(--line); border-radius:14px; padding:14px 16px; min-width:0; }
.note h2 { font-size:13px; letter-spacing:.06em; text-transform:uppercase; color:var(--soft); margin:0 0 8px; }
.note ul { margin:0; padding-left:18px; }
.note p { margin:0; }
.layout { display:grid; grid-template-columns:220px minmax(0,1fr); gap:28px; margin-top:28px; align-items:start; }
nav.pages { position:sticky; top:calc(env(safe-area-inset-top, 0px) + 16px); display:flex; flex-direction:column; gap:2px; }
nav.pages a { color:var(--ink); text-decoration:none; padding:7px 10px; border-radius:10px; font-size:15px; }
nav.pages a:hover { background:var(--surface); }
nav.pages a .legal-dot { color:var(--brand); font-size:12px; margin-left:4px; }
a { color:var(--brand); }
:focus-visible { outline:2px solid var(--brand); outline-offset:2px; border-radius:6px; }
section.page { border-top:2px solid var(--ink); padding-top:14px; margin-bottom:44px; scroll-margin-top:16px; }
.phead { display:flex; flex-wrap:wrap; gap:8px 14px; align-items:baseline; }
.phead h2 { margin:0; font-size:26px; line-height:1.15; font-weight:800; }
.phead .slugs { font-family:var(--mono); font-size:12px; color:var(--soft); }
.legal-banner { background:var(--legal-bg); border-radius:12px; padding:10px 14px; margin:12px 0 0; font-size:14px; }
.cols { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:24px; margin-top:16px; }
.col { background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:18px 22px; min-width:0; }
.col .lang { font-family:var(--mono); font-size:12px; letter-spacing:.06em; color:var(--soft); text-transform:uppercase; }
.col .title { font-size:22px; font-weight:800; margin:4px 0 2px; line-height:1.2; }
.col .desc { color:var(--soft); font-size:14px; margin:0 0 10px; }
.col h3 { font-size:19px; margin:22px 0 6px; line-height:1.25; }
.col h4 { font-size:16px; margin:16px 0 4px; }
.col p, .col li { max-width:68ch; }
.col ul { padding-left:20px; }
.ref { font-family:var(--mono); font-size:11px; color:var(--soft); border:1px solid var(--line); border-radius:6px; padding:0 5px; margin-left:6px; white-space:nowrap; vertical-align:1px; }
mark.field { background:var(--field-bg); color:var(--field-ink); font-family:var(--mono); font-size:13px; border-radius:5px; padding:0 4px; }
.toggle { display:none; }
footer { color:var(--soft); font-size:14px; margin-top:24px; max-width:80ch; }
@media (max-width:900px) {
  .layout { grid-template-columns:1fr; }
  nav.pages { position:static; flex-direction:row; flex-wrap:wrap; }
  .cols { grid-template-columns:1fr; }
}
"""

def path(lang, page):
    return f'/{lang}/' + (f'{page["slug"]}/' if page['slug'] else '')

def anchor(page):
    return page['slug'] or 'inicio'

def page_html(pt, en):
    legal = pt.get('legal')
    banner = ('<p class="legal-banner"><b>Versão para revisão jurídica</b> (decisão 271). Na fase fechada vale como aviso aos convidados; '
              'antes da abertura ao público passa pela revisão da decisão 228. O texto em português é o que vale (268).</p>') if legal else ''
    cols = ''
    for lang, p in (('pt', pt), ('en', en)):
        cols += (f'<article class="col" lang="{"pt-BR" if lang == "pt" else "en"}"><div class="lang">{lang} · {path(lang, p)}</div>'
                 f'<div class="title">{inline(p["title"])}</div><p class="desc">{inline(p["description"])}</p>{render(p["body"])}</article>')
    return (f'<section class="page" id="{anchor(pt)}"><div class="phead"><h2>{inline(pt["title"])}</h2>'
            f'<span class="slugs">{path("pt", pt)} · {path("en", en)}</span></div>{banner}<div class="cols">{cols}</div></section>')

def main():
    pt, en = read('pt'), read('en')
    assert [p['order'] for p in pt] == [p['order'] for p in en], 'pt and en must have the same pages'
    fields = sorted({f for p in pt + en for f in FIELD.findall(p['body'] + p['title'] + p['description'])})
    nav = ''.join(f'<a href="#{anchor(p)}">{inline(p["title"])}{"<span class=legal-dot>§</span>" if p.get("legal") else ""}</a>' for p in pt)
    pages = ''.join(page_html(a, b) for a, b in zip(pt, en))
    words = sum(len(re.sub(r'<!--.*?-->', '', p['body']).split()) for p in pt)
    out = f'''<title>Textos do Site VGR</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;700;800&family=Atkinson+Hyperlegible+Mono:wght@400&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <p class="eyebrow">Rodada 25 · S1 · decisões 267–275</p>
  <h1>Textos do site do VGR, para revisão</h1>
  <p class="lede">As {len(pt)} páginas do site em <b>português e inglês, lado a lado</b>. Ao fim de cada parágrafo, os números das decisões de onde ele vem.
  Os campos em <mark class="field">DESTAQUE</mark> ainda faltam. Leia, peça ajustes, e aprove para a S2 construir o site.</p>
  <div class="notes">
    <div class="note"><h2>Faltam</h2><ul>{"".join(f"<li><mark class=field>{f}</mark></li>" for f in fields)}</ul></div>
    <div class="note"><h2>Como ler</h2><p>O português vale juridicamente; o inglês é tradução (268). As páginas marcadas com § são jurídicas: rascunho para a revisão da 228.</p></div>
    <div class="note"><h2>Tamanho</h2><p>{f"{words:,}".replace(",", ".")} palavras em português.</p></div>
  </div>
  <div class="layout">
    <nav class="pages" aria-label="Páginas">{nav}</nav>
    <main>{pages}</main>
  </div>
  <footer>Fonte: <code>vgr-ai/docs/site/textos/</code>. Esta página é gerada por <code>docs/site/revisao/build.py</code>.</footer>
</div>
'''
    with open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(out)
    print('pages', len(pt), 'fields', fields, 'words pt', words)

if __name__ == '__main__':
    main()
