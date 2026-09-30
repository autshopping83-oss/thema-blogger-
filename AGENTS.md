# Fluxo de Valor Blog — regras do agente

## Integração Blogger

Ferramentas MCP disponíveis sob o nome `blogger` (servidor `@dalcontak/blogger-mcp-server`).

Leitura: `list_blogs`, `get_blog`, `get_blog_by_url`, `list_posts`, `get_post`,
`search_posts`, `list_labels`, `get_label`.

Escrita: `create_post`, `update_post`, `delete_post`.

## Regras de escrita (obrigatórias)

| Ação | Permissão |
|------|-----------|
| READ | automática |
| CREATE (draft) | automática, sempre como rascunho |
| UPDATE | apenas quando pedido explicitamente |
| PUBLISH / unpublish / agendar | requer confirmação explícita do utilizador |
| DELETE | requer confirmação explícita com título + postId |

Nunca publiques, apagues ou edites posts sem confirmação prévia.

## Blog de trabalho

Sempre que uma operação precisar de `blogId`, usa o blog correto:

- `BLOGGER_ID`: preencher em `docs/blog-id.md` após o passo de descoberta.

Se o `blogId` não estiver confirmado, pergunta antes de executar qualquer escrita.

## Tema

O tema vive em `blogger/theme.xml` e é versionado no Git. O MCP **não** é usado
para trocar o template Blogger — tema é desenvolvido em Git + XML e aplicado
manualmente no Blogger (Blogger → Tema → ← Voltar/Restaurar).

## Fases

- **FASE 1 (concluída):** frontend local + `blogger/theme.xml`, sem qualquer
  contacto com a conta Blogger, API, OAuth ou MCP. No fim: parar e entregar
  relatório — não iniciar a FASE 2 sem pedido explícito.
- **FASE 2:** descoberta do `blogId`, publicação de conteúdo.
- **FASE 3:** Google Cloud OAuth + Blogger MCP + `opencode mcp list`.

## Segredos

Nunca escrevas `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` ou
`GOOGLE_CLIENT_ID` em ficheiros do projeto, no prompt ou em logs.
Segredos ficam apenas em `~/.config/blogger-mcp/env` (fora do Git).
