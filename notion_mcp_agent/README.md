# Notion MCP Agent

This folder contains a small example Python ADK agent that connects to Notion using the MCP (Model Context Protocol) via a Stdio (stdin/stdout) MCP server process.

This README explains how the Notion MCP integration is used to create the agent, why a stdio connection is used, how the MCP process is launched, environment setup, and troubleshooting notes.

## What this agent does

- Instantiates a Gemini LLM-backed agent (via the ADK `Agent` class).
- Uses a Notion MCP server process (the official `@notionhq/notion-mcp-server`) launched via `npx`.
- Communicates with the MCP server over stdin/stdout using a Stdio connection (no network socket required).
- Supplies Notion API headers (including the Notion integration secret) to the MCP server via environment variables.

The agent source is `agent.py` in this folder. It creates an `Agent` with an `MCPToolset` configured to start and talk to the Notion MCP server using `StdioServerParameters`.

## Key implementation points

- Environment variable: `NOTION_API_KEY` must be provided. The agent converts it into the JSON `OPENAPI_MCP_HEADERS` expected by the MCP server.
- The MCP server is started with `npx -y @notionhq/notion-mcp-server`. This is done by the `StdioServerParameters.command` + `args` in `agent.py`.
- The `MCPToolset` is created with `StdioConnectionParams` so the Python process and MCP server exchange messages over the subprocess' stdin/stdout streams.

Example snippets from `agent.py` (conceptually):

- Build Notion headers:

  - `NOTION_API_KEY = os.getenv("NOTION_API_KEY")`
  - `NOTION_MCP_HEADERS = json.dumps({"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"})`

- Start the MCP server via stdio:

  - `command = "npx"`
  - `args = ["-y", "@notionhq/notion-mcp-server"]`
  - `env = {"OPENAPI_MCP_HEADERS": NOTION_MCP_HEADERS}`

  These are passed into `StdioServerParameters` which is used by `StdioConnectionParams` inside the `MCPToolset`.

## Why use a Stdio MCP connection?

- Simplicity: launching the MCP server as a local subprocess and talking over stdin/stdout avoids the need to expose a network port or host a separate MCP server.
- Security: the Notion API key is only passed to the child process via an environment variable and not exposed to the network (as long as the machine is secure).
- Good for development and testing: it's easy to spin up and tear down the MCP server automatically from your Python code.

For production, you can also run the MCP server independently (for example on a remote host) and use an HTTP/streaming connection instead.

## Prerequisites

- Python 3.8+ and a virtual environment for the project.
- Node.js and npm (or at least `npx`) installed and available on your PATH. The agent uses `npx` to run `@notionhq/notion-mcp-server`.
- A Notion Integration API key (the integration must have the required permissions for the pages/databases you want to read).

## Setup

1. Create or activate a Python virtual environment and install your project dependencies (follow your project's `pyproject.toml` or requirements setup).

2. Create a `.env` file in the project root or set the following environment variable in your shell:

```powershell
$env:NOTION_API_KEY = "secret_your_notion_integration_token"
```

Or create a `.env` file containing:

```bash
NOTION_API_KEY=secret_your_notion_integration_token
```

3. Confirm `npx` is available:

```powershell
npx --version
```

If Node.js / npm is not installed, install it from https://nodejs.org/.

## Run the agent

From the parent repository root (or the folder containing the package), run the agent module. Example using PowerShell:

```powershell
# from parent repository root
adk web
```

When run, the Python code will:

1. Read `NOTION_API_KEY` and emit `OPENAPI_MCP_HEADERS` for the MCP server.
2. Launch `npx -y @notionhq/notion-mcp-server` as a subprocess.
3. Communicate with the MCP server using stdin/stdout.
4. Register MCP tools on the agent so it can perform Notion read/search/summarize actions when asked.

Note: The provided `agent.py` primarily wires up the agent and MCP toolset. You will typically call the agent's run loop or integrate it with your higher-level orchestration to send tasks/queries to it.

## Troubleshooting

- If the MCP server fails to start:
  - Ensure Node.js and `npx` are installed and on PATH.
  - Try running `npx -y @notionhq/notion-mcp-server` manually to see stderr output.
- If the agent can't access Notion:
  - Verify `NOTION_API_KEY` is set and the integration has access to the target pages/databases.
  - Validate the `Notion-Version` header if you rely on specific API behavior; the example uses `2022-06-28`.
- If the connection hangs or times out, consider increasing the `timeout` configured in `StdioConnectionParams`.

## Security and best practices

- Keep `NOTION_API_KEY` secret. Do not commit `.env` or API keys to source control.
- Use least-privilege integration scopes for Notion.
- For production use, consider running the MCP server in a managed or isolated environment and use a secure connection pattern appropriate for your deployment.

## Next steps and enhancements

- Add concrete example scripts that send sample MCP requests and show the agent summarizing a Notion page.
- Add unit/integration tests that mock the MCP server and verify the agent's tool wiring.
- Add an option to use a TCP/HTTP MCP connection instead of stdio for deployment scenarios.

## Where to look in the code

- `notion_mcp_agent/agent.py` — the code that creates the `Agent`, prepares `NOTION_MCP_HEADERS`, and configures `MCPToolset` with `StdioConnectionParams` and `StdioServerParameters`.

If you need an example of how to call the agent or how to wire the agent into a runtime loop, I can add a small runner script or tests next.

---

Created to document the Notion MCP stdio-based agent wiring and how to run it locally.

## Useful links

- Notion MCP server (source, docs, and examples): [Notion MCP server — GitHub](https://github.com/makenotion/notion-mcp-server)
