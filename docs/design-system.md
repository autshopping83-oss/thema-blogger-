# Design system

Tokens centralizados em `src/css/variables.css`; nada de valores mágicos
noutros ficheiros.

## Ficheiros CSS (ordem de carregamento)

| Ficheiro | Conteúdo |
|----------|----------|
| `reset.css` | box-sizing, margens, `img/svg` block, lista sem estilo |
| `variables.css` | tokens + overrides por breakpoint |
| `base.css` | tipografia, links, botões, campos, utilitários (`.container`, `.visually-hidden`, `.skip-link`, `.btn`, `.field`, `.eyebrow`, `.meta`) |
| `header.css` | `.site-header`, `.header-inner`, logo, ações |
| `navigation.css` | `.main-nav`, `.nav-list`, drawer/backdrop |
| `hero.css` | `.hero`, `.hero-grid`, `.hero-media` (16:9) |
| `cards.css` | `.card`, `.card-grid`, `.card-media` (16:9) |
| `sections.css` | `.section`, `.split`, `.newsletter`, `.ad-slot`, `.breadcrumb`, `.pagination`, `.search-*` |
| `calculators.css` | `.calc-*` (grelha 1/3/4 col., formulário em 2 col. ≥1024) |
| `article.css` | `.article-*`, `.faq`, `.related`, corpo do artigo |
| `sidebar.css` | `.sidebar`, widgets, `.recent-*`, `.category-list`, `.widget-calc` |
| `footer.css` | `.site-footer`, `.footer-grid`, `.footer-bottom` |
| `responsive.css` | os 4 media queries, por último |

## Tokens

**Cor** `--color-primary` / `-dark` / `-soft`, `--color-text`,
`--color-text-secondary` (uso restrito: fundos escuros, `#9CA3AF`),
`--color-text-strong` (`#4B5563`, para secundário sobre fundo claro),
`--color-text-muted`, `--color-background`, `--color-surface`,
`--color-border`, `--color-success`, `--color-danger`,
`--color-footer-*`.

**Tipografia** `--font-family` (system-stack), `--text-h1…--text-small`,
`--leading-tight/-heading/-body`, `--weight-regular/-medium/-semibold/-bold`.

**Layout** `--container-width`, `--container-gutter`, `--article-width`
(700–760px de texto), `--sidebar-width` (300px), `--header-height` (60/68px),
`--hero-image-share`.

**Espaço/raio** `--space-xs…--space-2xl`, `--space-section`,
`--radius-sm/-md/-lg`, `--shadow-sm/-md`.

**Motion/detalhe** `--transition-fast`, `--transition`, `--z-header`,
`--z-drawer`, `--target-min: 44px`.

## Componentes

- **Botões** `.btn--primary`, `.btn--secondary`, `.btn--ghost` + estado
  `:hover/:focus-visible/:active`.
- **Campos** `.field` + `.field-error` com `aria-invalid`/`aria-describedby`.
- **Cards** `.card` → `.card-media` (`aspect-ratio: 16/9`, `height: auto` na img),
  `.card-body` (eyebrow → título `h3` → resumo → meta).
- **Calculadoras** cartões `.calc-card` empilhados em mobile, linha a partir
  de 768px; `.calc-form` com `display: block` em mobile e 2 colunas ≥1024px.
- **Anúncios** `.ad-slot` com `aria-label` único por posição.
- **Widgets sidebar** `.widget-title` (`h2`), `.recent-list`,
  `.category-list` com contador, `.widget-calc` de destaque.
- **Header/Footer** container centrado, header sticky com `--z-header`,
  footer escuro com disclaimer.

## Padrões acessíveis

- Hierarquia de headings sem saltos; um `h1` por página.
- `aria-label` explícito onde o texto visível é só ícone.
- Foco sempre visível (`:focus-visible`), nunca `outline: none` sem substituto.
- Estados de erro/vazio com texto + `aria-live`, não só cor.
- Imagens `alt` descritivo, `loading="lazy"` fora da primeira dobra,
  `width`/`height` declarados para evitar layout shift.
