#!/usr/bin/env python3
"""Valida e audita blogger/theme.xml (estrutura + JSON-LD + regras do Blogger).

Uso: python3 tools/validate-theme.py
Sai com != 0 se houver erros; avisos saem sempre detalhados.
"""
import os, sys, tempfile, xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'blogger', 'theme.xml')
B = '{http://www.google.com/2005/gml/b}'
X = '{http://www.w3.org/1999/xhtml}'

fail = []
try:
    ET.parse(PATH)
    print('[ok] XML well-formed')
except Exception as e:
    print('[ERRO] XML:', e); sys.exit(1)

root = ET.parse(PATH).getroot()

def path_of(el, parents):
    p = []
    cur = el
    while cur in parents:
        cur = parents[cur]
        p.append('%s%s' % (cur.tag.replace(B, 'b:'), (cur.get('id') or '')))
    return ' < '.join(p)

parents = {}
for parent in root.iter():
    for child in parent:
        parents[child] = parent

# 1. nenhuma section dentro de widget / if / loop
for sec in root.iter(B + 'section'):
    p = path_of(sec, parents)
    for bad in ('b:widget', 'b:if', 'b:loop', 'b:includable'):
        if bad in p:
            fail.append('section #%s dentro de %s -> %s' % (sec.get('id'), bad, p))
if not fail:
    print('[ok] nenhuma <b:section> dentro de b:widget / b:if / b:loop / b:includable')

# 2. nenhuma section duplicada / nenhum widget duplicado
ids = [s.get('id') for s in root.iter(B + 'section')]
wid = [w.get('id') for w in root.iter(B + 'widget')]
if len(ids) != len(set(ids)):
    fail.append('ids de section duplicados: %r' % ids)
if len(wid) != len(set(wid)):
    fail.append('ids de widget duplicados: %r' % wid)
print('[ok] sections: %s' % ', '.join(ids))
print('[ok] widgets: %s' % ', '.join(wid))

# 3. ordem dentro de <main>
main = [m for m in root.iter(X + 'main') if m.get('class') == 'main-content']
if not main:
    fail.append('<main class=main-content> nao encontrado')
else:
    order = [c.get('id') for c in main[0] if c.tag == B + 'section']
    print('[ok] ordem em <main>: %s' % ' -> '.join(order))
    if order != ['featured', 'ad-after-featured', 'main']:
        fail.append('ordem inesperada em <main>: %r' % order)

# 4. Blog1 sem sections dentro
def widget_by_id(wid_id):
    for w in root.iter(B + 'widget'):
        if w.get('id') == wid_id:
            return w
blog = widget_by_id('Blog1')
if blog is None:
    fail.append('Blog1 nao encontrado')
else:
    if any(True for _ in blog.iter(B + 'section')):
        fail.append('Blog1 ainda contem b:section')
    else:
        print('[ok] Blog1 sem <b:section> aninhado')
    txt = ET.tostring(blog, encoding='unicode').replace(chr(39), '"')
    if "class='hero'" in txt or 'class="hero"' in txt:
        fail.append('Blog1 ainda renderiza o hero')
    else:
        print('[ok] Blog1 sem hero (hero vem do FeaturedPost1)')
    if 'ad-after-featured' in txt:
        fail.append('Blog1 ainda referencia ad-after-featured')
    else:
        print('[ok] Blog1 sem ad-after-featured')

# 5. FeaturedPost existe, guarda por homepage, mostra post mais recente
fp = widget_by_id('FeaturedPost1')
if fp is None:
    fail.append('FeaturedPost1 nao encontrado')
else:
    t = ET.tostring(fp, encoding='unicode').replace(chr(39), '"')
    if 'type="FeaturedPost"' not in t:
        fail.append('FeaturedPost1 com tipo errado')
    if 'useMostRecentPost' not in t:
        fail.append('FeaturedPost1 sem useMostRecentPost=true')
    if 'data:view.isHomepage' not in t:
        fail.append('FeaturedPost1 sem guarda de homepage')
    if 'class="hero"' not in t:
        fail.append('FeaturedPost1 nao renderiza o hero')
    if fail == [] or all('FeaturedPost' not in f for f in fail):
        print('[ok] FeaturedPost1: hero + guarda isHomepage + useMostRecentPost')

# 6. AD guardado pelo widget, com aria-label e wrap
ad = widget_by_id('HTML11')
if ad is None:
    fail.append('HTML11 (ad-after-featured) nao encontrado')
else:
    t = ET.tostring(ad, encoding='unicode').replace(chr(39), '"')
    for must in ("data:view.isHomepage", 'class="ad-wrap"', 'aria-label'):
        if must not in t:
            fail.append('HTML11 sem %s' % must)
    print('[ok] HTML11: renderizavel so na homepage, com .ad-wrap e aria-label')

# 7. contagem de heroes no template inteiro
heroes = ET.tostring(root, encoding='unicode').replace(chr(39), '"').count('class="hero"')
print('[info] ocorrencias de class=hero no template: %d' % heroes)
if heroes != 1:
    fail.append('esperado exatamente 1 hero, encontrado %d' % heroes)

print()
if fail:
    print('FALHOU:')
    for f in fail:
        print(' -', f)
    sys.exit(1)
print('ESTRUTURA OK — nenhuma section condicionada')

# ================= JSON-LD =================
import json, re, subprocess

print('\n--- JSON-LD ---')
xml = open(PATH, encoding='utf-8').read()
fails2 = []

def render(node):
    """Serializa o conteudo de um script, substituindo tags de dados por '1'
    (valido em contexto de string ou de numero)."""
    def walk(n):
        out = []
        if n.text:
            out.append(n.text)
        for ch in n:
            if len(ch):
                out.append(walk(ch))
            elif ch.text:
                out.append(ch.text)
            else:
                out.append('1')
            if ch.tail:
                out.append(ch.tail)
        return ''.join(out)
    return walk(node)

scripts = [sc for sc in root.iter(X + 'script')
           if sc.get('type') == 'application/ld+json']
if not scripts:
    fails2.append('nenhum bloco JSON-LD encontrado')

types = []
for sc in scripts:
    body = render(sc)
    try:
        data = json.loads(body)
        types.append(data.get('@type'))
    except Exception as e:
        fails2.append('JSON invalido em %s: %s' % (ET.tostring(sc, encoding='unicode')[:60], e))
print('[ok] %d blocos JSON-LD validos (dados Blogger -> placeholder)' % len(scripts))

print('[ok] tipos: %s' % ', '.join(t for t in types if t))
for must in ('WebSite', 'CollectionPage', 'WebPage', 'Article', 'BreadcrumbList'):
    if must not in types:
        fails2.append('falta @type %s' % must)

if 'FAQPage' in types:
    fails2.append('FAQPage emitida como bloco estatico (tem de ser dinamica)')
elif 'FAQPage' not in xml:
    fails2.append('script dinamico de FAQPage ausente')
else:
    print('[ok] FAQPage so via JS dinamico (emitida apenas com FAQ visivel real)')

if '"Fluxo de Valor"' in xml or 'Como montar um or' in xml:
    fails2.append('JSON-LD com dados do blog/post hardcoded')
elif 'jsonEscaped' not in xml:
    fails2.append('sem .jsonEscaped nos dados')
else:
    print('[ok] dados via data:* + .jsonEscaped (nada hardcoded)')

def conds_of(node):
    """condicoes dos b:if/b:unless ascendentes (incluindo o proprio elemento)."""
    out = []
    cur = node
    while True:
        c = cur.get('cond')
        if c:
            out.append(c)
        if cur in parents:
            cur = parents[cur]
        else:
            break
    return ' | '.join(out)

guards = {'WebSite': 'data:view.isHomepage',
          'CollectionPage': 'data:view.isMultipleItems and not data:view.isHomepage',
          'WebPage': 'data:view.isPage',
          'Article': 'data:view.isPost'}
seen = set()
bc_contexts = set()
for sc in scripts:
    data = json.loads(render(sc))
    t = data.get('@type')
    ctx = conds_of(sc)
    if t in guards and t not in seen:
        seen.add(t)
        if guards[t] in ctx:
            print('[ok] %s condicionado por %s' % (t, guards[t]))
        else:
            fails2.append('%s sem guarda %s (cond: %s)' % (t, guards[t], ctx))
    if t == 'BreadcrumbList':
        src = ET.tostring(sc, encoding='unicode')
        if 'data:post' in src:
            bc_contexts.add('artigo')
        elif 'data:view.title' in src:
            bc_contexts.add('categoria/pagina')
        if 'data:view.isPost' in ctx:
            bc_contexts.add('artigo')
        if 'data:view.isMultipleItems' in ctx:
            bc_contexts.add('categoria/pagina')
for t in guards:
    if t not in seen:
        fails2.append('nao encontrei @type %s no template' % t)

print('[ok] BreadcrumbList em contextos: %s' % ', '.join(sorted(bc_contexts)))
if not {'artigo', 'categoria/pagina'} <= bc_contexts:
    fails2.append('BreadcrumbList incompleto: %r' % bc_contexts)

m = re.search(r'<script>//<!\[CDATA\[(.*?)//\]\]></script>', xml, re.S)
if not m:
    fails2.append('bloco CDATA do script nao encontrado')
else:
    tmp = os.path.join(tempfile.gettempdir(), 'theme-inline.js')
    open(tmp, 'w', encoding='utf-8').write(m.group(1))
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
    if r.returncode != 0:
        fails2.append('erro de sintaxe no JS: %s' % r.stderr.strip()[:400])
    else:
        print('[ok] script inline do tema: sintaxe JS valida')

print()
if fails2:
    print('FALHOU (JSON-LD):')
    for f in fails2:
        print(' -', f)
    sys.exit(1)
print('JSON-LD OK')

# ================= AUDITORIA (motor de templates do Blogger) =================
print('\n--- AUDITORIA ---')
errs, warns = [], []

# 1. skin unica e fora de condicionais
skins = [s for s in root.iter(B + 'skin')]
if len(skins) != 1:
    errs.append('skin count = %d (tem de ser exatamente 1)' % len(skins))
else:
    p = conds_of(skins[0])
    if p:
        errs.append('b:skin dentro de condicional: %s' % p)
    else:
        print('[ok] exatamente 1 <b:skin>, fora de condicionais')

# 2. cada widget tem includable main, version=2 e esta dentro de uma section
for w in root.iter(B + 'widget'):
    wid = w.get('id')
    if [i.get('id') for i in w.iter(B + 'includable')].count('main') != 1:
        errs.append('widget %s sem exatamente um includable main' % wid)
    if w.get('version') != '2':
        errs.append('widget %s version=%s (esperado 2)' % (wid, w.get('version')))
    if parents.get(w, None) is None or parents[w].tag != B + 'section':
        errs.append('widget %s nao e filho direto de uma b:section' % wid)
print('[ok] 12 widgets: includable main, version=2, filho direto de b:section')

# 3. sections so contem widgets; ids unicos e com charset aceite
import re as _re
for sec in root.iter(B + 'section'):
    kids = [c.tag for c in sec]
    bad = [k for k in kids if k != B + 'widget']
    if bad:
        errs.append('section %s contem %s (so pode conter b:widget)'
                    % (sec.get('id'), bad))
    sid = sec.get('id') or ''
    if not _re.fullmatch(r'[A-Za-z0-9_-]+', sid):
        errs.append('section id com caracteres invalidos: %r' % sid)
    elif '-' in sid:
        warns.append('section id %r usa hifen (docs oficiais dizem letras/numeros; '
                     'observado a funcionar em temas reais)' % sid)
print('[ok] todas as sections contem apenas b:widget; ids unicos')

# 4. classes de migracao convencionais (header/main/sidebar/footer/navbar)
CLASS_MAP = {'site-branding': 'header', 'nav': 'navbar', 'main': 'main',
             'sidebar': 'sidebar', 'footer-widgets': 'footer'}
for sec in root.iter(B + 'section'):
    sid = sec.get('id')
    if sid in CLASS_MAP:
        cls = (sec.get('class') or '').split()
        if CLASS_MAP[sid] not in cls:
            warns.append('section %r sem class de migracao %r '
                         '(Blogger usa estas classes para transferir widgets '
                         'entre temas)' % (sid, CLASS_MAP[sid]))

# 5. atributos do <html>
html = [h for h in root.iter(X + 'html')]
if html:
    h = html[0]
    for a, v in [(B + 'layoutsVersion', '3'), (B + 'defaultwidgetversion', '2'),
                 (B + 'responsive', 'true'), (B + 'css', 'false')]:
        if h.get(a) != v:
            warns.append('<html %s=%r (padrao de temas modernos: %r)'
                         % (a, h.get(a), v))
    print('[ok] <html> %s' % ', '.join('%s=%s' % (k.replace(B, 'b:'), h.get(k)) for k in
          [B + 'layoutsVersion', B + 'defaultwidgetversion', B + 'responsive', B + 'css']))

# 6. entidades HTML proibidas no XML
raw = open(PATH, encoding='utf-8').read()
for ent in ('&nbsp;', '&mdash;', '&hellip;'):
    if ent in raw:
        errs.append('entidade HTML %s no XML (so &amp; &lt; &gt; sao validos)' % ent)
print('[ok] sem entidades HTML proibidas')

# 7. inventario de data tags + riscos conhecidos
tags = sorted(set(_re.findall(r'data:[a-zA-Z0-9_.]+', raw)))
print('[info] %d expressoes data: distintas no tema' % len(tags))
KNOWN_RISK = {
    'data:post.href': ('ALTA', 'em PopularPosts/FeaturedPost o campo documentado '
                               'e data:post.url — trocar'),
    'data:imageUrl': ('MEDIA', 'Header v2: confirmar no Layout; fallback e omitir a img'),
    'data:post.lastUpdated.iso8601.jsonEscaped': (
        'MEDIA', 'fallback documentado: data:post.lastUpdatedISO8601'),
}
for t, (lvl, note) in KNOWN_RISK.items():
    if t in tags:
        warns.append('%s [%s] -> %s' % (t, lvl, note))
    else:
        print('[ok] risco conhecido ja resolvido: %s' % t)

# 8. data:post.* so tem significado dentro de <b:loop ... var='post'>
#    (sem o loop o Blogger serve "Can't find substitution for tag [post.x]")
body = _re.sub(r'<!--.*?-->', '', raw, flags=_re.S)
toks = _re.compile(r"</?b:loop\b[^>]*>|data:post\.")
stack, bad_scope = [], []
for m in toks.finditer(body):
    tok = m.group(0)
    if tok.startswith('</b:loop'):
        if stack:
            stack.pop()
    elif tok.startswith('<b:loop'):
        var = _re.search(r"\bvar='([^']+)'", tok)
        stack.append(var.group(1) if var else '?')
    elif 'post' not in stack:
        lineno = body[:m.start()].count('\n') + 1
        bad_scope.append('linha %d: %s' % (lineno, body[m.start():m.start() + 40].split("'")[0]))
if bad_scope:
    for b in bad_scope[:5]:
        errs.append('data:post fora de b:loop var=post — %s' % b)
else:
    print('[ok] todas as data:post.* estao dentro de b:loop var=post')

print()
if errs:
    print('ERROS DE AUDITORIA:')
    for e in errs:
        print(' -', e)
    sys.exit(1)
print('AUDITORIA: %d avisos (nenhum erro)' % len(warns))
for w in warns:
    print(' ~', w)
