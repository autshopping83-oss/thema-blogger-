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
| Conteúdo | `main` → `Blog1` | hero, cards, categoria, post, breadcrumb, paginação |
| Anúncio | `ad-after-featured` → `HTML11` | entre hero e recentes (homepage) |
| Barra lateral | `sidebar` | `BlogSearch1`, `PopularPosts1`, `Label1`, `HTML20`, `HTML21` |
| Rodapé | `footer-widgets` → `HTML30` | links extra legais/categorias |
| Rodapé | estático | colunas, disclaimer, copyright |
| Script | inline | drawer acessível (foco, Escape, trap, backdrop) |

## Renderização condicional (`Blog1`)

- `isMultipleItems && isHomepage` → hero (1º post) + grelha de recentes (`i > 0`).
- `isMultipleItems && !isHomepage` → `page-header` + cards de categoria/arquivo/pesquisa.
- `!isMultipleItems` → post individual (breadcrumb, corpo, rótulos).
- Sempre: `pagination` (`newerPageUrl` / `olderPageUrl`).

## Verificar após importar

- [ ] Menu do `PageList` preenche o `nav-list` (criar as páginas em Blogger → Páginas).
- [ ] `Header1` mostra título (logo opcional via widget).
- [ ] Slots de anúncio vazios (HTML widgets) não partem o layout.
- [ ] Labels existem em **Rótulos** e aparecem no `Label1`.
- [ ] URLs relativas (`search`, `archive`, `p/...`) resolvem para `https://valorfacil.blogspot.com/`.
- [ ] Tema mobile (`?m=1`) e desktop (`?m=0`), 360/768/1280/1920.
- [ ] Drawer: `aria-expanded`, Escape, foco preso, sem scroll de fundo.
- [ ] Lighthouse: acessibilidade ≥ 95, sem violações axe.

## Notas técnicas

- IDs `HTML10/HTML11/HTML20/HTML21/HTML30` são estáveis — não renomear.
- `b:section` de anúncios vive dentro de `b:if` (homepage). Se o Blogger
  rejeitar, mover a seção para fora do condicional e esconder com CSS.
- Nenhuma entidade HTML (`&nbsp;`) no XML; tags vazias auto-fechadas (`<br/>`).
- Domínio canónico/OG já é `https://valorfacil.blogspot.com/` (em `src/` via
  constante; no tema via `data:blog.canonicalUrl`, dinâmico). Os caminhos
  (`/article.html`, `/category.html`) são os do preview local e passam a
  permalinks reais no deploy.
- `data:post.snippets.short` depende de o post ter resumo (Blogger → definições
  de post: "descrição manual" ou primeira linha).
