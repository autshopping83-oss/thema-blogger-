# Fluxo de Valor Blogger

Integração Google Cloud → OAuth 2.0 → Blogger MCP → OpenCode.

```
OpenCode ──stdio──> @dalcontak/blogger-mcp-server ──OAuth2──> Blogger API v3
   │
   └──Git──> theme/theme.xml ──> Blogger Theme
```

## Setup

1. Google Cloud: projeto + Blogger API v3 + OAuth Client (Web application,
   redirect `https://developers.google.com/oauthplayground`).
2. Refresh token via OAuth Playground.
3. Segredos em `~/.config/blogger-mcp/env` (chmod 600, fora do Git):

```bash
source ~/.config/blogger-mcp/env
env | grep '^GOOGLE_' | sed 's/=.*$/=<configured>/'
```

4. Testar:

```bash
source ~/.config/blogger-mcp/env
opencode mcp list
```

`blogger` deve aparecer como `connected`.

## Estrutura

- `opencode.json` — servidor MCP local (stdio), segredos via `{env:...}`
- `AGENTS.md` — regras de escrita/publicação do agente
- `docs/` — design system e IDs do blog
- `theme/` — template do Blogger versionado
- `preview/` — capturas de teste
