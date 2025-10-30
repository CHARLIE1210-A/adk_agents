# ADK Agents Repository

This repository contains example agents that demonstrate how to build LLM-backed agents using the ADK and the Model Connector Protocol (MCP). The examples show different MCP wiring styles (stdio subprocess, local mock servers, and other integrations).

Repository layout

- `example_agent/` — minimal example agent wiring.
- `google_map_mcp/` — an example agent demonstrating MCP usage for map/geolocation tooling.
- `mcp_example_agent/` — another MCP example showing how to expose tools to an agent.
- `mcp_local_example/` — local MCP example(s) for development and testing.
- `mcp_server/` — helper or example MCP server implementations (mock servers, utilities).
- `notion_mcp_agent/` — Notion MCP example showing how to launch the official Notion MCP server via `npx` and connect over stdio. See `notion_mcp_agent/README.md` for complete setup and run instructions.
- `wiki_agent/` — an agent example focused on wiki-style content and summarization.

Security

- Keep API keys out of source control. Use `.env` files or environment variables locally and secret stores in production.
- Limit integration scopes to least privilege.

Contributing

- Add a README to any new agent/example explaining how to run it and its required credentials.
- Consider small runner scripts and tests that exercise MCP wiring for each example.
