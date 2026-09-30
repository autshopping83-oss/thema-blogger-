# Tema Blogger — `theme.xml`

Template em formato Blogger Layouts (v2) que espelha o frontend local em `src/`.
Desenvolvido em Git; aplicado manualmente no Blogger.

## Como aplicar

1. Backup em **Blogger → Tema → ⋮ → Backup**.
2. **Blogger → Tema → ← Voltar/Restaurar → Submeter ficheiro** → `theme.xml`.
3. Guardar; verificar em `https://valorfacil.blogspot.com/?m=1` e `?m=0`.
4. Se o Blogger rejeitar o XML, usar a cópia limpa: validar antes com
   `python3 -c "import xml.etree.ElementTree as ET; ET.parse('blogger/theme.xml')"`.

> A FASE 1 termina aqui. Nenhuma dessas operações foi executada — o ficheiro
> está apenas versionado localmente.

## Estrutura

| Bloco | Seção / widget | Papel |
|-------|----------------|-------|
| `<head>` | `all-head-content`, `Header`, canonical | SEO, título condicional |
| Cabeçalho | `site-branding` → `Header1` | logo/título + link para home |
| Navegação | `nav` → `PageList1` | menu principal (páginas) |
| Anúncio topo | `ad-top` → `HTML10` | slot `ad-slot` acessível |
| Destaque/hero | `featured` → `FeaturedPost1` | hero da homepage (post mais recente) |
| Anúncio | `ad-after-featured` → `HTML11` | entre hero e recentes (só homepage) |
| Conteúdo | `main` → `Blog1` | recentes, categoria, post, breadcrumb, paginação |
| Barra lateral | `sidebar` | `BlogSearch1`, `PopularPosts1`, `Label1`, `HTML20`, `HTML21` |
| Rodapé | `footer-widgets` → `HTML30` | links extra legais/categorias |
| Rodapé | estático | colunas, disclaimer, copyright |
| Script | inline | drawer acessível (foco, Escape, trap, backdrop) |

## Renderização condicional (`Blog1`)

- `isMultipleItems && isHomepage` → grelha de recentes (`i > 0`, o 1º post é o
  destaque).
- `isMultipleItems && !isHomepage` → `page-header` + cards de categoria/arquivo/pesquisa.
- `!isMultipleItems` → post individual (breadcrumb, corpo, rótulos).
- Sempre: `pagination` (`newerPageUrl` / `olderPageUrl`).

Ordem das secções dentro de `<main>`: `featured` → `ad-after-featured` → `main`.

## Secções: regra estrutural

Todas as `<b:section>` são filhas diretas de um elemento normal (`div`/`main`/
`aside`) — **nunca** dentro de `<b:widget>`, `<b:if>` ou `<b:loop>`. O
conteúdo condicional (só homepage) é aplicado **dentro do `b:includable` do
widget**, que é seguro para o Blogger.

Verificação automática:

```bash
python3 /data/data/com.termux/files/usr/tmp/opencode/fvtest/structure.py
```

## Verificar após importar

- [ ] `FeaturedPost1` mostra o post mais recente (se vier vazio, em **Layout**
      escolher o post ou manter `useMostRecentPost=true`).
- [ ] O slot `ad-after-featured` aparece entre o hero e "Publicações recentes"
      na homepage e **não** aparece em categoria/artigo.
- [ ] Rich Results Test: `WebSite` na home, `CollectionPage`+`BreadcrumbList`
      em categoria, `Article`+`BreadcrumbList` num post, `FAQPage` só em
      artigos com `<details>` visíveis.
- [ ] Menu do `PageList` preenche o `nav-list` (criar as páginas em Blogger → Páginas).
- [ ] `Header1` mostra título (logo opcional via widget).
- [ ] Slots de anúncio vazios (HTML widgets) não partem o layout.
- [ ] Labels existem em **Rótulos** e aparecem no `Label1`.
- [ ] URLs relativas (`search`, `archive`, `p/...`) resolvem para `https://valorfacil.blogspot.com/`.
- [ ] Tema mobile (`?m=1`) e desktop (`?m=0`), 360/768/1280/1920.
- [ ] Drawer: `aria-expanded`, Escape, foco preso, sem scroll de fundo.
- [ ] Lighthouse: acessibilidade ≥ 95, sem violações axe.

## JSON-LD (dados estruturados)

Tudo dinâmico, a partir de `data:*` do próprio Blogger — nenhum valor fixo:

| Página | `@type` emitido | Origem dos dados |
|--------|-----------------|------------------|
| Homepage | `WebSite` + `SearchAction` | `data:blog.title`, `data:blog.homepageUrl` |
| Categoria/arquivo/pesquisa | `CollectionPage` + `BreadcrumbList` | `data:view.title`, `data:blog.canonicalUrl` |
| Página estática | `WebPage` + `BreadcrumbList` | `data:view.title` |
| Artigo (`data:view.isPost`) | `Article` + `BreadcrumbList` | `data:post.title`, `.snippets.short`, `.date.iso8601`, `.lastUpdated.iso8601`, `.author`, `.labels` |
| Artigo com FAQ visível | `FAQPage` | lido do DOM pelo script do tema |

- `FAQPage` **nunca** é emitida como bloco fixo: o script varre
  `details` dentro de `.article-body` e só cria o JSON-LD se encontrar
  perguntas visíveis (pergunta = `<summary>`, resposta = `.faq-answer`).
- Convenção de conteúdo no editor HTML do Blogger:

```html
<details class="faq-item">
  <summary>Pergunta?</summary>
  <div class="faq-answer"><p>Resposta.</p></div>
</details>
```

- Strings escapadas com `.jsonEscaped` (títulos, URLs, resumos) para o JSON
  não partir com aspas ou acentos.

## Notas técnicas

- IDs `HTML10/HTML11/HTML20/HTML21/HTML30` e `FeaturedPost1` são estáveis —
  não renomear.
- O Blogger envolve cada secção num `<div class="... section">`; por isso o
  espaçamento de secções usa `section.section` (e não `.section`) para os
  wrappers vazios não criarem buracos na página.
- Nenhuma entidade HTML (`&nbsp;`) no XML; tags vazias auto-fechadas (`<br/>`).
- Domínio canónico/OG já é `https://valorfacil.blogspot.com/` (em `src/` via
  constante; no tema via `data:blog.canonicalUrl`, dinâmico). Os caminhos
  (`/article.html`, `/category.html`) são os do preview local e passam a
  permalinks reais no deploy.
- `data:post.snippets.short` depende de o post ter resumo (Blogger → definições
  de post: "descrição manual" ou primeira linha).
