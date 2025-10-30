import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# It's good practice to define paths dynamically if possible,
# or ensure the user understands the need for an ABSOLUTE path.
# For this example, we'll construct a path relative to this file,
# assuming '/path/to/your/folder' is in the same directory as agent.py.
# REPLACE THIS with an actual absolute path if needed for your setup.
CURRENT_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DSA_FOLDER_PATH = "C:\\Users\\91789\\Desktop\\DSA"
DEV_FOLDER_PATH = "C:\\Users\\91789\\Desktop\\Dev"
PROJECT_FOLDER_PATH = os.path.expanduser("~/Desktop/Project")
# print(f"Using CURRENT_FOLDER_PATH: {CURRENT_FOLDER_PATH}")
# print(f"Using DSA_FOLDER_PATH: {DSA_FOLDER_PATH}")
# Ensure TARGET_FOLDER_PATH is an absolute path for the MCP server.

root_agent = Agent(
    model='gemini-2.0-flash',
    name='filesystem_assistant_agent',
    instruction='Help the user manage their files. You can list files, read files, etc.',
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",  # Argument for npx to auto-confirm install
                        "@modelcontextprotocol/server-filesystem",
                        # IMPORTANT: This MUST be an ABSOLUTE path to a folder the
                        # npx process can access.
                        # For example: "/Users/youruser/accessible_mcp_files"
                        # or use a dynamically constructed absolute path:
                        os.path.abspath(CURRENT_FOLDER_PATH),
                        os.path.abspath(DSA_FOLDER_PATH),
                        os.path.abspath(DEV_FOLDER_PATH),
                        os.path.abspath(PROJECT_FOLDER_PATH),
                    ],
                ),
                timeout=20,
            ),
            # Optional: Filter which tools from the MCP server are exposed
            # tool_filter=['list_directory', 'read_file']
        )
    ],
)