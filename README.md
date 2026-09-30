# Fluxo de Valor — blog (Blogger)

Frontend estático + template Blogger para `https://valorfacil.blogspot.com`,
desenvolvido em fases. FASE 1 concluída: **só trabalho local, sem qualquer
contacto com a conta Blogger, API, OAuth ou MCP.**

```
OpenCode ──stdio──> @dalcontak/blogger-mcp-server ──OAuth2──> Blogger API v3   (FASE 3)
   │
   └──Git──> blogger/theme.xml ──> Blogger Tema                                 (FASE 2)
```

## Fases

| Fase | Conteúdo | Estado |
|------|----------|--------|
| **1** | Frontend local (`src/`) + `blogger/theme.xml`, testes e docs | **concluída** |
| 2 | Descoberta do `blogId`, publicação de conteúdo | por iniciar |
| 3 | Google Cloud + OAuth + Blogger MCP + `opencode mcp list` | preparada, pausada |

A FASE 1 termina com relatório. Nenhuma operação sobre a conta Blogger foi
(nem pode ser) executada até à FASE 2.

## Estrutura

- `src/` — `index.html`, `article.html`, `category.html`, `search.html`,
  `css/` (13 ficheiros), `js/` (main, navigation, search), `assets/images/`
- `blogger/theme.xml` + `blogger/README.md` — template e instruções de import
- `docs/` — `architecture.md`, `design-system.md`, `blogger-mapping.md`
- `preview/` — capturas de ecrã geradas pelos testes
- `AGENTS.md` — regras de escrita/publicação do agente
- `opencode.json` — servidor MCP local (FASE 3)

## Correr localmente

```bash
python3 -m http.server 8080 --bind 127.0.0.1   # workdir: src/
# http://127.0.0.1:8080/
```

Sem build, sem `npm install` no projeto — o site é HTML/CSS/JS puro.

## Testes

O harness vive fora do repo, em
`/data/data/com.termux/files/usr/tmp/opencode/fvtest/` (puppeteer-core +
Chromium):

```bash
node test.js        # 5 páginas × 10 larguras + interações + axe-core
node axe-detail.js  # detalhe de violações (se houver)
node shots.js       # screenshots full-page
```

Resultado da FASE 1: **todos os testes passaram**, axe-core com **zero
violações**.

Validação do template:

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('blogger/theme.xml'); print('xml ok')"
```

## Setup (FASE 3 — ainda não executado)

1. Google Cloud: projeto + Blogger API v3 + OAuth Client (Web application,
   redirect `https://developers.google.com/oauthplayground`).
2. Refresh token via OAuth Playground.
3. Segredos em `~/.config/blogger-mcp/env` (chmod 600, fora do Git):

```bash
source ~/.config/blogger-mcp/env
env | grep '^GOOGLE_' | sed 's/=.*$/=<configured>/'
opencode mcp list    # `blogger` deve aparecer como `connected`
```

Conta de destino: `aut.shopping83@gmail.com` · Blog: `https://valorfacil.blogspot.com`.
