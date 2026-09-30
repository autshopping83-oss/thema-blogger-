# Arquitetura — FASE 1

Frontend estático, sem build: HTML5 + CSS3 + JS vanilla + SVG inline.
Zero frameworks, zero dependências externas (fonts system-stack).

```
projects/fluxo-de-valor-blog/
├── src/                     site local (pré-visualização)
│   ├── index.html           homepage
│   ├── article.html         artigo (breadcrumb, calculadora, FAQ, JSON-LD)
│   ├── category.html        categoria/arquivo (main + sidebar)
│   ├── search.html          resultados de pesquisa (?q=)
│   ├── css/                 13 ficheiros (ver docs/design-system.md)
│   ├── js/                  main, navigation, search
│   └── assets/images/       logo.svg + 5 placeholders 16:9
├── blogger/
│   ├── theme.xml            template Blogger (espelha src/)
│   └── README.md            como aplicar + checklist de verificação
├── docs/                    arquitetura, design system, mapeamento
├── preview/                 capturas de ecrã (geradas)
├── opencode.json            servidor MCP (FASE 3, vazio)
├── AGENTS.md                regras do agente
└── README.md                visão geral e fases
```

## Páginas

| Página | Ficheiro | Estrutura |
|--------|----------|-----------|
| Home | `index.html` | hero (1º post) → ad → recentes (cards) → split de categoria → calculadoras → secções → newsletter |
| Artigo | `article.html` | breadcrumb → cabeçalho → figura → corpo → rótulos → FAQ → relacionados → JSON-LD |
| Categoria | `category.html` | `page-header` + grelha de cards + `.main-layout` com sidebar |
| Pesquisa | `search.html` | campo, contagem, resultados, estado vazio |

`category.html` e `search.html` partilham o `main-layout` (70/30 → 280px sidebar).

## Sistema responsivo

Quatro breakpoints oficiais (`src/css/responsive.css`):

| Range | Papel |
|-------|-------|
| `≤767px` | mobile — drawer, grelhas a 1 coluna, hero empilhado |
| `768–1023px` | tablet — grelhas a 2/3 colunas |
| `1024–1279px` | desktop — sidebar fixa, grelha de cards a 3/4 |
| `≥1280px` | large — container máx., escala tipográfica ↑ |

Blocos partilhados desktop usam `min-width: 1024px` (cobre 1024/1280/1366/1440/1920).

Toda a escala (tipografia, espaço, header) é redefinida em `variables.css`
dentro desses breakpoints — nunca números soltos.

## JavaScript

Sem dependências; progressive enhancement — as páginas funcionam sem JS.

- `navigation.js` — drawer acessível: `aria-expanded`, foco inicial, trap com
  Tab/Shift+Tab, fecho com Escape, backdrop, `body.overflow=hidden`, restauro
  do foco anterior.
- `main.js` — validação da newsletter (mensagem por `aria-live`), calculadora
  de demonstração (juros compostos), ano dinâmico do copyright.
- `search.js` — dataset fictício (~20 entradas), filtro por termo, render de
  resultados com destaque `<mark>`, contagem, estado vazio, URL `?q=`.

## SEO e acessibilidade

- Um único `h1` por página; hierarquia `h2 → h3` sem saltos.
- `meta description`, canonical, Open Graph/Twitter e JSON-LD (Article,
  Breadcrumb, FAQPage) sobre `https://valorfacil.blogspot.com/` — os
  caminhos (`/article.html`, `/category.html`) são os do preview local e
  passam a permalinks reais no deploy. No preview o JSON-LD é estático;
  em `blogger/theme.xml` é gerado a partir de `data:*` (ver
  `blogger/README.md`).
- Landmarks: `header`/`nav`/`main`/`aside`/`footer`, skip-link, foco visível.
- Alvos ≥ 44px (`--target-min`), contraste AA verificado com axe-core.

## Testes (local)

Harness em `/data/data/com.termux/files/usr/tmp/opencode/fvtest/`
(puppeteer-core + Chromium, fora do repo):

```bash
python3 -m http.server 8080 --bind 127.0.0.1   # workdir src/
node test.js                                    # responsividade + interações + axe
node axe-detail.js                              # detalhe de violações
node shots.js                                    # screenshots em shots/
python3 tools/validate-theme.py                             # estrutura do theme.xml + JSON-LD
```

Cobertura: 5 páginas × 10 larguras (360→1920), overflow horizontal, imagens,
erros de consola/404, `h1` único, header 60/68px, grelhas 1/3/4, footer 1/4,
`aspect-ratio` 16:9, sidebar 300px, texto 700–760px, pesquisa, drawer,
newsletter, calculadora — e axe-core com **zero violações**.
