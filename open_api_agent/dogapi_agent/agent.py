import json
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
# --- OpenAPI Tool Imports ---
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

# Load environment variables if present
load_dotenv()

# Constants
AGENT_NAME_OPENAPI = "dogapi_manager_agent"
GEMINI_MODEL = "gemini-2.5-pro"

# Read the OpenAPI spec as a JSON string (preserve original formatting)
with open("dogapi_agent\dogapi.json", "r", encoding="utf-8") as f:
    openapi_spec_string = f.read()

# Create OpenAPIToolset from the Dog API spec
dogapi_toolset = OpenAPIToolset(
    spec_str=openapi_spec_string,
    spec_str_type='json',
)

# Agent Definition
root_agent = LlmAgent(
    name=AGENT_NAME_OPENAPI,
    model=GEMINI_MODEL,
    tools=[dogapi_toolset],
    instruction="""You are a Dog API assistant. Use the provided OpenAPI-based tools
to answer user requests about dog breeds, groups, and facts. When listing breeds or
groups, mention pagination or filters (e.g., `page[number]`, `page[size]`). When
returning facts, respect the `limit` parameter and indicate how many facts were
requested. When a specific ID is requested, confirm the ID in your response.
""",
    description="Manages Dog API operations using tools generated from `dogapi.json`."
)
