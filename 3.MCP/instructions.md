# Instructions

This document provides setup instructions and helpful notes for working with MCP (Model Context Protocol) materials.

---

## UV: Python Package & Project Manager

We will use **[uv](https://docs.astral.sh/uv/)** — a lightning-fast Python package and project manager written in Rust.

### Installation  
Refer to the official documentation for installation instructions:  
🔗 https://docs.astral.sh/uv/

### Common Commands

```shell
# Initialize a new project
uv init <project_name> <directory>

# Create a virtual environment with Python 3.11
uv venv --python 3.11

# Activate the environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Add a package to your project
uv add <package_name>

# Use pip with uv
uv pip install <package_name>

# Remove a package
uv remove <package_name>

# Run a Python script
uv run script.py

# View dependency tree
uv tree
```


## FastMCP 

MCP provides SDKs in multiple languages. In this tutorial, we will use the **Python SDK**.

📦 GitHub Repository: [https://gofastmcp.com/getting-started/installation](https://gofastmcp.com/getting-started/installation)

### Installation

To install the MCP Python SDK using `uv`:

```shell
uv pip install fastmcp
```

<br><br><br><br><br>

# MCP Host Candidates

Below is a curated list of tools you can use as **MCP hosts** — i.e., platforms capable of managing context, tools, and prompts via the [Model Context Protocol](https://github.com/modelcontextprotocol).

---

### Claude Desktop
- **Type:** Desktop app (GUI)
- **Description:** Local GUI client for Anthropic’s Claude models.
- **MCP Use:** Can be extended with plugins to serve as a full MCP host.
- **Link:** [https://claude.ai](https://claude.ai)

---

### CrewAI
- **Type:** Multi-agent task coordination
- **MCP Use:** Tools and prompts can be mapped to MCP entities.
- **Features:** Roles, memory, structured tool use.
- **Link:** [https://github.com/joaomdmoura/crewAI](https://github.com/joaomdmoura/crewAI)

---

### OpenAgents
- **Type:** Multi-agent system using OpenAI Assistants API
- **MCP Use:** Supports extension into MCP-compatible architecture.
- **Features:** Agent planner, web search, retrieval, code execution.
- **Link:** [https://github.com/OpenAgents](https://github.com/OpenAgents)

---

###  AutoGen
- **Type:** Conversational agents framework by Microsoft
- **MCP Use:** Can act as host or client depending on orchestration.
- **Features:** Agents communicating with each other and humans.
- **Link:** [https://github.com/microsoft/autogen](https://github.com/microsoft/autogen)

---

###  Ollama
- **Type:** Local LLM runner
- **MCP Use:** Useful as a local model backend for MCP tools.
- **Features:** Fast, offline, works well with MCP SDK.
- **Link:** [https://ollama.com](https://ollama.com)

---
