# Filesystem MCP Agent

This folder contains a small example agent that demonstrates how to connect an ADK LLM agent to a filesystem-focused MCP server using a Stdio (stdin/stdout) MCP connection.

The example shows how to launch the MCP server package `@modelcontextprotocol/server-filesystem` via `npx` and pass absolute folder paths to the MCP server so it can list and read files under those folders.

File to look at

- `filesystem_mcp_agent/agent.py` — constructs an `Agent`, configures an `MCPToolset` with `StdioConnectionParams`, and launches the MCP server with `npx`.

Key points

- The MCP server is launched by calling `npx -y @modelcontextprotocol/server-filesystem` and passing folder paths as additional command-line arguments.
- The filesystem MCP server requires ABSOLUTE paths to folders that the subprocess can access. The example `agent.py` sets several example absolute paths (e.g. `C:\Users\91789\Desktop\DSA`).
- Communication between the Python process and the MCP server is over the subprocess' stdin/stdout using `StdioConnectionParams`.
- A short timeout is configured in the example (`timeout=20` seconds) — increase if your filesystem or startup is slow.

Why absolute paths?

- The MCP subprocess is an independent process. Relative paths may be resolved differently depending on the child process' working directory. Providing absolute paths guarantees the MCP server resolves the target folders correctly.

Prerequisites

- Python 3.8+ and a virtual environment for the project.
- Node.js and npm (so `npx` is available) — the agent uses `npx` to run the filesystem MCP server.

Configuration notes

- Edit `filesystem_mcp_agent/agent.py` to set the folder paths you want the MCP server to expose. Use absolute paths. Example variables used in the file:

  - `DSA_FOLDER_PATH = "C:\\Users\\91789\\Desktop\\DSA"`
  - `DEV_FOLDER_PATH = "C:\\Users\\91789\\Desktop\\Dev"`
  - `PROJECT_FOLDER_PATH = os.path.expanduser("~/Desktop/Project")`

- You may prefer to build these paths dynamically from environment variables or a configuration file for portability.

How the MCP command is formed (conceptual)

- The example constructs the subprocess command like:

  ```text
  npx -y @modelcontextprotocol/server-filesystem <abs_path_1> <abs_path_2> <abs_path_3> ...
  ```

  The MCP subprocess will then expose tools that operate on the listed directories (for example: `list_directory`, `read_file`).

Run the agent (example, PowerShell)

```powershell
# from parent repository root
adk web
```

Before running the Python agent, you can test the MCP server invocation manually to see startup logs and confirm paths:

```powershell
# Run the MCP server directly to inspect output
npx -y @modelcontextprotocol/server-filesystem C:\Users\91789\Desktop\DSA
```

Troubleshooting

- MCP server fails to start or exits immediately:
  - Ensure Node.js / npm / `npx` is installed and on PATH.
  - Run the `npx` command directly (see previous section) to inspect stderr for permission errors or path errors.
- Tools missing or not exposed:
  - Confirm the filesystem MCP server supports the tools you expect (list/read). Check package docs or run the server manually to inspect advertised tools.
- Permission denied when reading files:
  - Make sure the user account running the Python process and the spawned MCP subprocess has OS-level read permissions for the directories you supplied.
- Connection timeouts or hangs:
  - Increase the `timeout` in `StdioConnectionParams` in `agent.py`.

Security and best practices

- Limit which folders you expose to the MCP server. Do not pass root (`C:\`) or other sensitive system folders.
- Run MCP servers with least privilege; consider creating a dedicated user account for agents that need file access.
- Never commit secrets or sensitive absolute paths to source control. Use configuration files or environment variables stored securely.

Next steps and enhancements

- Add a `tool_filter` in the `MCPToolset` configuration to expose only the specific tools you need (for example, only `list_directory` and `read_file`).
- Add a small runner script that demonstrates a sample query (e.g., list a directory and read a small file) and prints the response.
- Add unit/integration tests that mock or run the MCP server in a controlled temp directory to validate behavior.

Questions or help

If you'd like, I can:

- Add a small `runner.py` that demonstrates listing and reading a file via the MCP tools.
- Add test scaffolding that spins up the MCP server pointing at a temporary directory and validates the exposed tools.


## Useful links

- Filesystem MCP server (source, docs, and examples): [Filesystem MCP server — GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
