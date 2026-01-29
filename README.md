# AI Agent Platform POC

A proof-of-concept multi-agent platform built with LangChain and LangGraph, featuring dynamic agent orchestration, tool integration, and intelligent workflow management.

## 🌟 Features

- **Multi-Agent Architecture**: Build complex workflows with multiple specialized agents
- **Dynamic Agent Handoffs**: Seamlessly transfer tasks between agents based on context
- **Triage System**: Intelligent routing of requests to appropriate specialized agents
- **Tool Integration**: Extensible tool system for agent capabilities
- **Template-Based Configuration**: Define workflows declaratively using JSON templates
- **LangGraph Integration**: Leverage stateful agent workflows with visual graph representation

## 🏗️ Architecture

The platform consists of several key components:

- **Agent Builder**: Dynamically creates agents from template configurations
- **Node Builder**: Constructs agent nodes with proper tool and subagent assignments
- **Graph Builder**: Orchestrates agent workflows and manages state transitions
- **Tool Builder**: Provides a registry of available tools for agents
- **Template System**: JSON-based workflow definitions for easy customization

### Example Workflow

```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ▼
┌─────────────┐
│   Triage    │──────┐
│    Agent    │      │
└──────┬──────┘      │
       │             │
   ┌───┴────┬────────┴────────┐
   │        │                 │
   ▼        ▼                 ▼
┌──────┐ ┌─────────┐ ┌─────────────┐
│Tech  │ │Billing  │ │  General    │
│Agent │ │Agent    │ │  Support    │
└──┬───┘ └────┬────┘ └──────┬──────┘
   │          │              │
   └──────────┴──────────────┘
              │
              ▼
          ┌──────┐
          │ End  │
          └──────┘
```

## 📋 Prerequisites

- Python 3.12 or higher
- OpenAI API key
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Docker and Docker Compose (optional, for containerized deployment)

## 🚀 Installation

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver, written in Rust.

1. **Install uv** (if not already installed):

   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone the repository**:

   ```bash
   git clone https://github.com/IbadurRehman-kodexolab/aiagentplatformPOC.git
   cd aiagentplatformPOC
   ```

3. **Create a virtual environment and install dependencies**:

   ```bash
   uv venv
   uv pip install -e .
   ```

4. **Activate the virtual environment**:

   ```bash
   # On Windows
   .venv\Scripts\activate

   # On macOS/Linux
   source .venv/bin/activate
   ```

### Using pip (Alternative)

```bash
git clone https://github.com/IbadurRehman-kodexolab/aiagentplatformPOC.git
cd aiagentplatformPOC
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Using Docker (Containerized)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/IbadurRehman-kodexolab/aiagentplatformPOC.git
   cd aiagentplatformPOC
   ```

2. **Create a `.env` file** with your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Build and run with Docker Compose**:

   ```bash
   # Build the image
   docker-compose build

   # Run the application
   docker-compose up

   # Run in detached mode
   docker-compose up -d

   # View logs
   docker-compose logs -f
   ```

4. **For development with shell access**:

   ```bash
   # Start development container
   docker-compose --profile dev run --rm aiagent-dev

   # Or using docker directly
   docker-compose run --rm aiagent-dev /bin/bash
   ```

5. **Stop the containers**:

   ```bash
   docker-compose down
   ```

## ⚙️ Configuration

1. **Create a `.env` file** in the project root:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Customize your workflow** by editing `src/template.py` or creating your own template.

## 🐳 Docker Commands

### Building and Running

```bash
# Build the Docker image
docker-compose build

# Run the application
docker-compose up

# Run in background
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f aiagent

# Restart the service
docker-compose restart aiagent
```

### Development Mode

```bash
# Start development container with shell
docker-compose --profile dev run --rm aiagent-dev

# Run specific Python script
docker-compose run --rm aiagent python src/agent_builder.py

# Install new dependencies
docker-compose run --rm aiagent uv pip install <package-name>
```

### Rebuilding After Changes

```bash
# Rebuild image after dependency changes
docker-compose build --no-cache

# Rebuild and restart
docker-compose up --build
```

## 💻 Usage

### Basic Example

```python
from src.agent_builder import build_agent, SimpleGraphBuilder
from src.template import multi_agent_template
from langchain.messages import HumanMessage

# Build agents from template
created_agents = build_agent(multi_agent_template)

# Create the graph
graph = SimpleGraphBuilder(created_agents, multi_agent_template)

# Run a query
response = graph.invoke(
    {"messages": [HumanMessage(content="I need help with my account")]}
)

print(response)
```

### Running the Demo

```bash
python src/agent_builder.py
```

This will:
1. Create a multi-agent workflow with a triage agent and specialized agents
2. Generate a graph visualization (`graph.png`)
3. Process a sample customer query

## 🔧 Available Tools

The platform includes several built-in tools (defined in `src/tool_builder.py`):

- **get_weather**: Retrieve weather information for a city
- **get_news**: Fetch news on a specific topic
- **get_stock_price**: Get current stock prices

### Adding Custom Tools

Create new tools using LangChain's `@tool` decorator:

```python
from langchain.tools import tool

@tool
def my_custom_tool(param: str) -> str:
    """Description of what the tool does"""
    # Your implementation here
    return result
```

Then add your tool to the `tools` list in `tool_builder.py`.

## 📁 Project Structure

```
aiagentplatformPOC/
├── src/
│   ├── agent_builder.py    # Core agent creation and graph building logic
│   ├── template.py          # Workflow template definitions
│   └── tool_builder.py      # Tool registry and definitions
├── main.py                  # Entry point
├── pyproject.toml           # Project configuration and dependencies
├── uv.lock                  # Dependency lock file (uv)
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose orchestration
├── .dockerignore           # Docker ignore rules
├── .env                     # Environment variables (not in repo)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🛠️ Key Components

### Agent Builder

The `agent_builder.py` module provides:

- **`build_agent(template)`**: Creates agents from template configuration
- **`NodeBuilder(template)`**: Builds agent nodes with proper dependencies
- **`SimpleGraphBuilder(agents, template)`**: Constructs executable workflows
- **`create_handoff_tool()`**: Generates inter-agent handoff capabilities

### Template Structure

Templates define workflows declaratively:

```python
{
    "workflow": {
        "global_config": {
            "default_model": "gpt-4o",
            "checkpointer": {"enabled": False}
        },
        "nodes": [
            {
                "id": "agent_id",
                "type": "agent_node",
                "name": "agent_name",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "Your role...",
                    "tools": ["tool1", "tool2"],
                    "subagents": ["subagent1"]
                }
            }
        ],
        "edges": [
            {"from": "node1", "to": "node2"}
        ]
    }
}
```

## 🎯 Use Cases

- **Customer Support**: Route queries to specialized support agents
- **Data Processing Pipelines**: Chain agents for complex data transformations
- **Multi-Step Workflows**: Orchestrate sequential or parallel agent tasks
- **Decision Trees**: Implement conditional logic with agent handoffs
- **Research Assistants**: Coordinate specialized agents for comprehensive analysis

## 🚢 Deployment

### Docker Deployment

The project includes Docker support for easy deployment:

**Features:**
- Multi-stage build with uv for fast dependency installation
- Non-root user for enhanced security
- Optimized image size using Python slim base
- Volume mounting for development
- Environment variable configuration

**Production Deployment:**

```bash
# Build production image
docker build -t aiagent-platform:latest .

# Run production container
docker run -d \
  --name aiagent-platform \
  --env-file .env \
  aiagent-platform:latest
```

**Environment Variables:**

Create a `.env` file with the following:

```env
OPENAI_API_KEY=your_api_key_here
# Add other environment variables as needed
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Dependencies

- **langchain** (1.2.6): Framework for building LLM applications
- **langchain-openai** (≥1.1.7): OpenAI integration for LangChain
- **langgraph** (≥1.0.7): State machine orchestration for agents
- **langgraph-prebuilt** (≥1.0.7): Pre-built components for LangGraph
- **python-dotenv** (≥1.2.1): Environment variable management

## 📄 License

This project is provided as-is for proof-of-concept purposes.

## 👥 Author

**Ibadur Rehman** - [IbadurRehman-kodexolab](https://github.com/IbadurRehman-kodexolab)

## 🔗 Links

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [uv Package Manager](https://github.com/astral-sh/uv)

## 🙏 Acknowledgments

- Built with [LangChain](https://www.langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by OpenAI's GPT models
- Package management by [uv](https://github.com/astral-sh/uv)

---

**Note**: This is a proof-of-concept project. For production use, consider adding error handling, monitoring, rate limiting, and proper security measures.
