# Auditoria FASE 2 — `blogger/theme.xml`

Revisão do tema **antes** de qualquer instalação no Blogger. Nada foi instalado;
nenhum conteúdo foi publicado; a conta `aut.shopping83@gmail.com` não foi usada.

## 1. Âmbito e método

| Camada | Como | Resultado |
|--------|------|-----------|
| XML / estrutura | `python3 tools/validate-theme.py` (validador + auditor) | **0 erros, 12 avisos** |
| Frontend local | `node test.js` (5 páginas × 10 larguras + axe) | todos passam |
| Comportamento do tema | análise estática das regras do motor (§3) | ver §4 |
| **Só no Blogger** | upload real, Layout, `?m=1`, Rich Results Test | **pendente (§9)** |

Reproduzir a auditoria:

```bash
python3 tools/validate-theme.py
```

Cobertura: XML bem formado · secções fora de `b:widget`/`b:if`/`b:loop` · ordem
em `<main>` · 12 widgets com `includable main`, `version=2` e filho direto de
`b:section` · secções só com `b:widget` · ids únicos · exatamente 1 `b:skin`
fora de condicionais · sem entidades HTML proibidas · 7 blocos JSON-LD
sintaticamente válidos com guardas de contexto · JS inline com sintaxe válida ·
inventário de 49 expressões `data:`.

## 2. Inventário

**8 secções** (todas de nível de topo, filhas de `div`/`main`/`aside`):

| `id` | `class` | Widgets |
|------|---------|---------|
| `site-branding` | `site-branding` | `Header1` (locked) |
| `nav` | `nav-section` | `PageList1` |
| `ad-top` | `ad-section` | `HTML10` |
| `featured` | `featured-section` | `FeaturedPost1` |
| `ad-after-featured` | `ad-section` | `HTML11` |
| `main` | `main-section` | `Blog1` (locked) |
| `sidebar` | `sidebar-section` | `BlogSearch1`, `PopularPosts1`, `Label1`, `HTML20`, `HTML21` |
| `footer-widgets` | `footer-section` | `HTML30` |

## 3. Motor de templates do Blogger — regras confirmadas

Fontes: docs oficiais [Page elements tags for layouts](https://support.google.com/blogger/answer/46888),
[GeekThis – Structure of Custom Blogger Themes](https://geekthis.net/post/structure-of-custom-blogger-themes/),
lista de erros de validação do editor e JSON de runtime de temas reais.

1. **Uma secção só pode conter widgets.** "To insert extra code within a
   section, split the section into two or more new sections."
2. **Widgets têm de estar dentro de uma secção** — erro: *"The widget with id
   X is not within a section."*
3. **Cada widget precisa de um `b:includable id='main'`** (é o que é chamado
   para renderizar) e de `id` único; cada secção precisa de `id` único.
4. **Pelo menos uma secção e exatamente um `b:skin`** — erros: *"A theme must
   have at least one b:section tag"*, *"there should be one and only one skin
   in the template."*
5. **`class` convencionais** (`navbar`, `header`, `main`, `sidebar`, `footer`)
   são o que o Blogger usa para **transferir widgets quando se muda de tema**.
6. **`widget-settings` são validados no save** — nome inválido ⇒ *"The widget
   settings in widget with id X is not valid"* e o tema não guarda.
7. **Secções são "encontradas" pelo parser em elementos normais** (`div`,
   `main`…), mas **não dentro de elementos personalizados** (ex.: web
   components) — prática segura: nunca aninhar secções em widgets, condicionais
   ou loops.
8. **`b:class`** acrescenta classes à etiqueta anterior (permite condicionar o
   layout sem mexer na estrutura de secções).
9. **`b:responsive='true'` + `b:layoutsVersion='3'` + `b:defaultwidgetversion='2'`**
   é o padrão de temas modernos; com responsivo ativo o Blogger serve o mesmo
   tema em `?m=1`.
10. **`b:css='false'`** desliga o CSS por defeito do Blogger — o tema é o único
    responsável pelo estilo (widgets adicionados depois entram sem estilos).

Runtime `view` observado em tema real (JSON do Blogger): `isHomepage`,
`isPost`, `isPage`, `isMultipleItems`, `isSingleItem`, `isArchive`,
`isLabelSearch`, `isError` — **todas as guardas usadas no tema existem**.
Mesmo runtime confirma `homepageUrl`, `canonicalUrl`, `canonicalHomepageUrl`.

## 4. Limitações reais do motor (e a decisão do tema)

| # | Limitação | Consequência prática | Como o tema contorna |
|---|-----------|----------------------|----------------------|
| 1 | Secção só contém widgets; nada de HTML/ads solto dentro | **Impossível injetar um anúncio a meio do conteúdo do `Blog1`** (hero → ad → recentes) | Hero movido para `FeaturedPost1`; ad é secção própria entre as duas secções |
| 2 | Secção não pode viver dentro de `b:if`/`b:loop` | Não dá para mostrar/ocultar uma **zona de widgets** por página | Condição dentro do `b:includable` do widget **+** ocultar o wrapper com CSS (`b:class`) |
| 3 | Não há parser do HTML do post no servidor | Não dá para gerar `FAQPage`/dados do artigo a partir do corpo | `Article`/`Breadcrumb` a partir de `data:*`; `FAQPage` lida no cliente pelo DOM |
| 4 | `widget-settings` validados no save | Um nome errado **rejeita o tema inteiro** | Nomes de `FeaturedPost1` copiados de um dump real (`useMostRecentPost`, `showPostTitle`, `showSnippet`, `showFirstImage`) |
| 5 | `id` de widget não pode ser alterado depois | Renomear = widget novo, perde configuração | IDs estáveis documentados em `blogger/README.md` |
| 6 | Migração entre temas usa as `class` convencionais | Sem elas, os widgets não são transferidos se o utilizador trocar de tema | Avisado (§5) — correção aditiva pendente |
| 7 | Sem build; CSS só em `b:skin`, JS em `CDATA` | Sem SCSS/bundler; `<` e `&` partem o XML se não estiverem em `CDATA` | Design system espelhado no `b:skin`; JS todo em `//<![CDATA[ … //]]>` |
| 8 | Modelo de dados limitado a `data:` + `b:if/b:loop/b:eval/b:include/b:class` | Sem expressões arbitrários, sem acesso externo | Só campos documentados/observados (registo em §5) |
| 9 | Responsivo único (`b:responsive`) | Não existe tema `m.` separado | 4 breakpoints em CSS |
| 10 | Comentários, feeds, AdSense são widgets próprios com CSS do Blogger | Fora do perímetro do tema atual | Não incluídos; acrescentar widgets e CSS se forem usados |

## 5. Registo de riscos — assunções não verificáveis offline

Confiança = probabilidade de o tema guardar e renderizar sem erro.

| Expressão / decisão | Onde | Confiança | Evidência | Ação |
|---|---|---|---|---|
| `data:view.isPost`, `.isPage`, `.isLabelSearch`, `.isHomepage`, `.isMultipleItems` | guardas | **Alta** | presentes no JSON de runtime do Blogger | manter |
| `data:blog.canonicalHomepageUrl` | JSON-LD | **Alta** | runtime + tema real (jettheme) | manter |
| `data:post.date.iso8601` + `.jsonEscaped` | Article | **Alta** | snippets `blog-posts-gadget-v2` + exemplos reais | manter |
| `data:post.snippets.short` | hero/cards/Article | Média | documentado para Blog/FeaturedPost v2 | manter; se falhar, `data:post.body snippet` |
| ~~`data:post.lastUpdated.iso8601`~~ → `data:post.date.iso8601` | `dateModified` | Alta (aplicado) | campo já usado em `datePublished` | **resolvido (§7.4)** |
| `data:imageUrl` (Header v2) | logo | Média | guardado por `<b:if cond='data:imageUrl'>` | confirmar no Layout |
| ~~`data:post.href`~~ → `data:post.url` | `PopularPosts1` recentes | Alta (aplicado) | campo documentado para PopularPosts/FeaturedPost | **resolvido (§7.2)** |
| `FeaturedPost1` + `widget-settings` | hero | Média | nomes vindos de dump real | validar no 1º upload |
| `resizeImage(img, 1200, "1200:630")` | Article | Alta | API standard do tema | manter |
| `b:class cond='…'` | layout | Alta | documentado | manter |
| ids de secção com hífen (`ad-after-featured`…) | 4 secções | Alta | "letras e números" nas docs, mas temas reais usam hífen e o editor aceita | manter; renomear só se o save falhar |
| ~~`class` convencionais ausentes~~ | 5 secções | Alta (aplicado) | `header`/`navbar`/`main`/`sidebar`/`footer` acrescentadas | **resolvido (§7.3)** |

## 6. Divergência `src/` ↔ tema: a sidebar

**Factos (verificados no código):**

| Página | `src/` | tema atual |
|--------|--------|------------|
| `index.html` | sem sidebar, hero a largura total | sidebar + coluna estreita ❌ |
| `article.html` | sem sidebar | sidebar ❌ |
| `search.html` | sem sidebar | sidebar ❌ |
| `category.html` | `.container.main-layout` + sidebar | sidebar ✅ |

**Causa:** o tema tem `<div class='container main-layout'>` e
`<aside class='sidebar'>` **incondicionais** — a sidebar aparece em todas as
páginas e o conteúdo fica sempre numa coluna de ~70%.

**Restrição do motor (§4.2):** não se pode envolver a `<b:section>` da sidebar
num `<b:if>` — seria a segunda violação da regra "secções só com widgets, fora
de condicionais". A saída legal é **condicionar a classe do contentor e esconder
a sidebar em CSS**.

**Resolução proposta (patch, ainda não aplicado):**

```diff
-<div class='container main-layout'>
+<div class='container'>
+  <b:class cond='data:view.isLabelSearch or data:view.isArchive' name='main-layout'/>
   <main class='main-content' id='conteudo'>
```

```diff
   /* no <b:skin>, junto às regras de layout */
+  .container:not(.main-layout) > .sidebar{display:none}
```

Efeito por página: home/artigo/pesquisa → sem sidebar e conteúdo a largura
total (igual ao `src/`); etiqueta/arquivo → sidebar ✓.

**Trade-off:** os widgets da sidebar continuam no DOM mas ocultos com
`display:none` (não contam para leitores de ecrã nem para o axe). Aceitável;
alternativa seria duplicar o markup ou mover a secção, ambas piores.

**Alternativas rejeitadas:** `<b:if>` sobre a secção (viola §3.1/§3.7) ·
duplicar o `<aside>` por página (manutenção dupla) · manter a sidebar em todo
o lado (diverge do `src/` e aperta o artigo para <700px).

## 7. Correções — aplicadas nesta iteração (local; nada no Blogger)

| # | Correção | Tipo | Risco | Esforço |
|---|----------|------|-------|---------|
| 1 | **Sidebar condicional** (patch §6) | estrutural | médio | 2 edições + 1 regra CSS |
| 2 | **`data:post.href` → `data:post.url`** em `PopularPosts1` | data tag | alto se falhar | 1 linha |
| 3 | **Classes de migração** `header`/`navbar`/`main`/`sidebar`/`footer` (aditivas; sem colisão de CSS à exceção de `sidebar`, que é inclusivamente desejável — passa a aplicar o `gap` aos widgets) | aditivo | baixo | 5 atributos |
| 4 | `dateModified`: `lastUpdated.iso8601` → fallback `lastUpdatedISO8601` (ou `date.iso8601` como último recurso) | data tag | médio | 1 linha |
| 5 | *(opcional)* ids de secção sem hífen | estrutural | baixa | renomear 4 ids |

Aplicadas por esta ordem, todas só em `src/` + `blogger/theme.xml`:

1. ✅ **2** — `data:post.href` → `data:post.url` (`PopularPosts1`).
2. ✅ **1** — sidebar condicional: `<b:class cond='data:view.isLabelSearch or
   data:view.isArchive' name='main-layout'/>` + `.container:not(.main-layout) > .sidebar{display:none}`
   (skin **e** `src/css/sidebar.css`). A `<b:section id='sidebar'>` mantém-se
   sempre no markup com os 5 widgets nativos (`BlogSearch1`, `PopularPosts1`,
   `Label1`, `HTML20`, `HTML21`) — não foi transformada em markup fixo.
3. ✅ **3** — classes de migração `header`/`navbar`/`main`/`sidebar`/`footer`.
4. ✅ **4** — `dateModified` passa a `data:post.date.iso8601` (campo
   confirmado; a regressão era arriscar o save do tema). *Nota:* para posts
   editados depois de publicados, `dateModified` fica igual a `datePublished` —
   trocar por `lastUpdated` só depois de confirmado no Blogger.

A 5 (ids sem hífen) mantém-se opcional — só se o editor acusar erro no save.

**Verificação após aplicar** (`validate-theme.py` → 0 erros, **5 avisos**,
antes 12):

| Pedido | Resultado |
|---|---|
| XML bem formado | ✅ |
| Validação estrutural | ✅ secções de topo, ordem `featured → ad-after-featured → main` |
| Teste das 5 páginas / 10 breakpoints | ✅ `node test.js` — todos |
| canonical/OG/JSON-LD | ✅ 4 canonical + 4 `og:url` em `src/`; 7 blocos JSON-LD válidos no tema |
| `AD_AFTER_FEATURED` no lugar | ✅ entre hero e recentes; ausente fora da homepage |
| Screenshots antes/depois (home, artigo, categoria, 360/1440) | ✅ **6/6 byte a byte idênticos** |
| Sidebar em widgets nativos | ✅ `sidebar-rule.test.js`: 5 widgets, `display:none` sem `main-layout`, `flex` com ele (`preview/sidebar-sem-layout.png`) |

## 8. Checklist pré-instalação (gate)

- [ ] `tools/validate-theme.py` → **0 erros** e avisos §7 resolvidos ou aceites.
- [ ] XML válido (`ElementTree`) e `node --check` do JS inline.
- [ ] `node test.js` verde e capturas sem regressões.
- [ ] `blogger/README.md` com o checklist de verificação pós-import atualizado.
- [ ] **Backup do tema atual** em `valorfacil.blogspot.com` (Blogger → Tema → ⋮ → Backup) — guardado localmente.
- [ ] Plano de rollback definido: reverter para o backup em <2 min.
- [ ] Decidido se a instalação é feita por si (manual) ou pelo agente (requer FASE 3/MCP).

## 9. Plano de instalação (só depois do gate de §8)

Princípios: **tema de backup primeiro, cópia de teste, zero conteúdo novo.**

1. Backup do tema atual do blog (ficheiro `.xml`) + cópia local em `preview/backup/`.
2. Upload de `blogger/theme.xml` (Blogger → Tema → ← Voltar/Restaurar).
3. Se o editor rejeitar: ler a mensagem (§5 dá a hipótese mais provável —
   `widget-settings` ou id com hífen), corrigir, repetir. **Nunca** submeter
   por cima sem backup.
4. Verificar **sem publicar nada**: Layout (8 secções/widgets visíveis),
   home/categoria/artigo/pesquisa em `?m=1` e `?m=0` (360/768/1280/1920),
   drawer, busca, paginação, `FeaturedPost1`, slot `ad-after-featured`,
   breadcrumb, Rich Results Test (WebSite/CollectionPage/Article/FAQPage),
   axe-core no site real.
5. Registar resultados em `docs/theme-audit.md` (secção "verificação real").
6. Rollback imediato para o backup em qualquer falha.
7. Só depois: FASE 2b (conteúdo/`blogId`) e FASE 3 (OAuth + MCP).

## 10. Estado

- FASE 1: **concluída** (frontend + tema, testes e docs versionados).
- FASE 2 (esta): auditoria **concluída**; correções §7.1–§7.4 **aplicadas e
  verificadas**; instalação **não executada** (falta o gate de §8).
- Conta Blogger, MCP e OAuth: **intocados**.
