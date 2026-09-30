# Mapeamento `src/` → `blogger/theme.xml`

O tema espelha o frontend local: mesmas classes, mesmos tokens (copiados para
o `<b:skin>`), mesmos breakpoints. Só muda de onde vêm os dados.

## Estrutura

| Local (src) | Blogger | Origem dos dados |
|-------------|---------|------------------|
| `.site-logo` (Header) | `b:section#site-branding` → `Header1` | `data:title`, `data:imageUrl` |
| `.nav-list` | `b:section#nav` → `PageList1` | páginas do Blogger |
| `.ad-slot` topo | `b:section#ad-top` → `HTML10` | widget HTML (manual) |
| hero (homepage) | `b:section#featured` → `FeaturedPost1` | `data:posts` (post mais recente) |
| `.ad-slot` pós-hero | `b:section#ad-after-featured` → `HTML11` | widget HTML (manual) |
| recentes (homepage) | `Blog1` (`isHomepage`, `i > 0`) | `data:posts`, `data:post.snippets.short` |
| categoria/arquivo/pesquisa | `Blog1` (`isMultipleItems`) | `data:posts` + `data:view.title` |
| post individual | `Blog1` (único) | `data:post.body`, `data:post.labels` |
| paginação | includable `pagination` | `newerPageUrl`, `olderPageUrl` |
| sidebar | `b:section#sidebar` | `BlogSearch1`, `PopularPosts1`, `Label1`, `HTML20`, `HTML21` |
| footer widgets | `b:section#footer-widgets` → `HTML30` | manual |
| footer estático | markup | `data:blog.title` |
| `navigation.js` drawer | `<script>` inline | puro DOM |

## Classes partilhadas

Mantêm o mesmo nome nos dois lados: `.site-header`, `.header-inner`,
`.main-nav`, `.hero`, `.hero-grid`, `.hero-media`, `.section`,
`.section-header`, `.section-title`, `.card-grid`, `.card`, `.card-media`,
`.card-body`, `.card-title`, `.card-summary`, `.card-meta`, `.eyebrow`,
`.meta`, `.main-layout`, `.main-content`, `.sidebar`, `.widget-title`,
`.widget-calc`, `.recent-list`, `.category-list`, `.ad-slot`, `.breadcrumb`,
`.pagination`, `.article-*`, `.site-footer`, `.footer-grid`, `.footer-links`,
`.footer-bottom`, `.skip-link`, `.visually-hidden`, `.btn`, `.field`.

Se uma classe mudar em `src/`, a mesma alteração tem de ser aplicada em
`blogger/theme.xml`.

## Diferenças deliberadas

- **`.hero-title` é `h1`** só na homepage; no post o `h1` é `.article-title`.
- **`.card-title` é `h3`** na homepage e **`h2`** em categoria/arquivo (para a
  hierarquia partir do `h1` da `page-header`).
- Imagens usam `resizeImage(post, w, "16:9")` em vez de ficheiros locais.
- Anúncios e links legais são widgets manuais, não HTML fixo.
- **JSON-LD**: em `src/` é estático (demo); no tema é dinâmico — `WebSite`,
  `CollectionPage`/`WebPage`, `Article` e `BreadcrumbList` vêm de `data:*`
  (`.jsonEscaped`), e `FAQPage` é construída no cliente a partir das
  `<details>` visíveis do corpo do artigo. Ver `blogger/README.md`.

## Ficheiros de referência

- `src/index.html`, `src/article.html`, `src/category.html`, `src/search.html`
- `blogger/theme.xml`, `blogger/README.md`
- `docs/design-system.md`
