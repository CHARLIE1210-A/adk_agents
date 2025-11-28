# Dog API Agent

Overview
--------

This project contains a small Python agent that uses an OpenAPI-based toolset to interact with a Dog API specification (`dogapi.json`). The agent is implemented in `agent.py` and uses the ADK `LlmAgent` together with an `OpenAPIToolset` generated from the OpenAPI specification.

The agent's responsibilities:
- Load the OpenAPI spec (JSON) and convert it into a toolset.
- Expose the toolset to an LLM agent (`LlmAgent`) so the model can call API endpoints.

Files
-----
- `agent.py`: Main agent script. Creates an `OpenAPIToolset` from `dogapi.json` and instantiates an `LlmAgent`.
- `dogapi.json`: OpenAPI specification for the Dog API (used to build the toolset).
- `__init__.py`: package marker.

Requirements
------------

The code uses these Python libraries (suggested):

- Python 3.8+
- `python-dotenv` (for `.env` loading)
- Google ADK Python SDK (project-specific ADK that provides `google.adk.agents` and `google.adk.tools.openapi_tool`)

Example `requirements.txt` (suggested)

```
python-dotenv>=0.21.0
# The Google ADK package name may be internal; replace with the correct package or install instructions
# google-adk
```

If the ADK package isn't available via PyPI, follow your organization's installation instructions for the ADK (wheel, private index, or local package).

Environment & Credentials
-------------------------

The project calls `load_dotenv()` in `agent.py`, so you can place environment variables in a `.env` file in the project root. Typical variables you may need:

- `GOOGLE_API_KEY` or similar credentials required by the ADK (check your ADK docs)
- Any model selection variables or endpoint configuration required by your ADK installation

Create a `.env` file example:

```
# .env
# GOOGLE_API_KEY=YOUR_ADK_API_KEY
# OTHER_ADK_CONFIG=...
```

Setup (Windows PowerShell)
--------------------------

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (adjust if `google-adk` is private)

```powershell
pip install -r requirements.txt
# or if no requirements file:
pip install python-dotenv
# pip install google-adk  # if available
```

Running the Agent
-----------------

From the project parent root (where dogapi_agent -  `agent.py` and `dogapi.json` live), run:

```powershell
adk web
```

Notes about `agent.py` path usage
---------------------------------

`agent.py` currently reads the OpenAPI spec with the call:

```python
with open("dogapi_agent\\dogapi.json", "r", encoding="utf-8") as f:
    openapi_spec_string = f.read()
```

Because `agent.py` resides in the same directory as `dogapi.json`, this relative path may be incorrect depending on where you run the script from. Recommended fixes:

- Use a relative filename that references the same directory, e.g. `open("dogapi.json", ...)` if you run from that folder.
- Or join paths using `os.path.dirname(__file__)` to make the path robust:

```python
import os
BASE_DIR = os.path.dirname(__file__)
spec_path = os.path.join(BASE_DIR, "dogapi.json")
with open(spec_path, "r", encoding="utf-8") as f:
    openapi_spec_string = f.read()
```

OpenAPIToolset and Agent Behavior
---------------------------------

The project constructs an `OpenAPIToolset` via:

```python
dogapi_toolset = OpenAPIToolset(
    spec_str=openapi_spec_string,
    spec_str_type='json',
)
```

This toolset exposes the Dog API operations as callable tools for the `LlmAgent`. The `LlmAgent` is instantiated with the toolset in `agent.py`:

```python
root_agent = LlmAgent(
    name=..., model=..., tools=[dogapi_toolset], instruction=..., description=...
)
```

Behavioral notes for the agent (documented in the `instruction` string in `agent.py`):

- When listing breeds or groups, the agent mentions pagination options (e.g., `page[number]`, `page[size]`).
- When returning facts, it respects the `limit` parameter and indicates how many facts were requested.
- When a specific ID is requested, the agent confirms the ID in the response.

Usage Examples
--------------

Because the agent exposes the OpenAPI-backed tools to an LLM, you interact with it by providing natural language prompts that map to API operations. Example prompts (conceptual):

- "List dog breeds in the Herding group, page 1, 20 per page."
- "Get facts about Labrador Retrievers, limit 5."
- "Fetch details for breed with ID 123 and confirm that ID." 

Testing & Development
---------------------

- Add unit tests around how the spec is loaded and how the `OpenAPIToolset` is constructed.
- When iterating on the agent's prompt behavior, update the `instruction` in `agent.py` and restart the script.

Troubleshooting
---------------

- If imports fail for `google.adk.*`, ensure the ADK SDK is installed and available in the active environment.
- If the model cannot be reached, check API keys and ADK configuration in your `.env`.
- If file-not-found errors occur for `dogapi.json`, verify the script working directory or update `agent.py` to compute the path robustly (see recommended fix above).

