# Páginas institucionais (FASE 2b)

Fragmentos HTML para colar no editor de páginas do Blogger. Cada ficheiro é o
**corpo da página** — o tema envolve-o automaticamente em breadcrumb,
`article-header` (h1 = título da página) e `.article-body` (tipografia do
artigo). Não incluem `<html>`, `<head>` nem CSS.

| Ficheiro | Título da página | URL obrigatória |
|----------|------------------|-----------------|
| `sobre.html` | `Sobre` | `https://valorfacil.blogspot.com/p/sobre.html` |
| `privacidade.html` | `Privacidade` | `https://valorfacil.blogspot.com/p/privacidade.html` |
| `termos.html` | `Termos de uso` | `https://valorfacil.blogspot.com/p/termos.html` |

> Os links do rodapé (coluna **Legal**, dentro do tema) já apontam para estas
> três URLs — se o *slug* gerado não for este, o link continua em 404.

## Como criar (manual, sem API)

1. **Blogger → Páginas → Nova página**.
2. Título: `Sobre` (ou `Privacidade`, `Termos de uso`).
3. Alternar o editor para **HTML** (botão `< >`) e colar o conteúdo do
   ficheiro correspondente, **sem** nada mais.
4. **Link permanente → Personalizado** e escrever o *slug*:
   `sobre`, `privacidade`, `termos`.
   - O Blogger pode não oferecer *slug* personalizado em páginas. Se não
     oferecer, **avisa**: ou se cria a página `Termos` (slug `termos`) ou eu
     ajusto o link do rodapé para `/p/termos-de-uso.html` e voltas a submeter
     o tema.
5. Publicar (as páginas ficam acessíveis por link, sem aparecer como posts).
6. Repetir para as outras duas.

## Depois de publicar as três

1. **Layout → Menu principal** (widget `PageList1`): editar e marcar as três
   páginas (hoje só aparece “Página inicial”).
2. Coluna **Legal** do rodapé: já está ligada — só é preciso confirmar que os
   três links respondem 200.

## Verificação (só leitura, feita pelo agente)

```bash
for u in /p/sobre.html /p/privacidade.html /p/termos.html; do
  curl -sL -o /dev/null -w "%{http_code} $u\n" "https://valorfacil.blogspot.com$u"
done
```

Esperado: `200` nos três, mais `axe` a 0–1 violações (`page-has-heading-one`
não se aplica — cada página tem `h1` pelo próprio título) e
`WebPage`+`BreadcrumbList` no JSON-LD.

## Antes de preencher com o teu nome

- Se quiseres identificar a autoria ou dar um email de contacto, edita
  `sobre.html` (secção “Quem faz isto”) — hoje está escrita de forma genérica
  para não inventar dados.
- Datas: os textos usam `30 de setembro de 2026`; actualizar quando mudarem.
