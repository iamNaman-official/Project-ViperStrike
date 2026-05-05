# 🐍 Project ViperStrike: AI-Powered Agent Workspace

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)](https://github.com/iamNaman-official/Project-ViperStrike)
[![Smolagents](https://img.shields.io/badge/Smolagents-latest-orange?logo=python)](https://github.com/smol-ai/smolagents)

## Introduction

**Project ViperStrike** is my personal sandbox workspace for experimenting, building, and having fun with AI agents. Currently diving deep into [smolagents](https://github.com/smol-ai/developer) for creating intelligent, tool-equipped agents. **I have started learning from [Hugging Face](https://huggingface.co/), special thanks to Hugging Face for the amazing Agents Course!** Using [LiteLLM](https://litellm.vercel.app/) to unify models across providers, including testing agents using locally running AI models. Soon exploring new frameworks and one day building my own!

This repo showcases resilient multi-tier AI agents with fallback mechanisms, custom tools, and real-world demos.

## Features
- 🚀 **Multi-Tier Model Fallback**: Primary (Groq Llama 3.1 8B), Secondary (NVIDIA NIM Llama 3.1 70B), Local (Ollama Llama 3.1 8B)
- 🛠️ **Advanced Tool Integration**: Web search (DuckDuckGo), webpage visiting/scraping, custom tools (diagnostics, party planning, superhero themes)
- 🔍 **RAG & Tool Calling Agents**: Simple RAG with search/scrape, structured tool calling
- ✅ **Service Health Checks**: Automatic API availability checks for Groq, NVIDIA NIM, Ollama
- 🔐 **Secure Env Management**: .env keys with masked logging
- 📊 **Observability**: Langfuse integration for tracing (HuggingFaceAgent)
- 🎉 **Fun Demos**: Superhero party planning, system diagnostics, web research

## Tech Stack
| Category | Technologies |
|----------|--------------|
| **Framework** | smolagents (CodeAgent, ToolCallingAgent) |
| **Model Proxy** | LiteLLM |
| **LLMs** | Groq (Llama 3.1 8B Instant), NVIDIA NIM (Llama 3.1 70B), Ollama (Llama 3.1 8B) |
| **Tools** | DuckDuckGoSearchTool, WebSearchTool, VisitWebpageTool, custom @tool |
| **Infra** | NVIDIA NIM API, Groq API, Ollama local |
| **Observability** | Langfuse, OpenInference |
| **Utils** | python-dotenv, requests |

<details>
<summary>🐍 Project Structure</summary>

```
Project-ViperStrike/
├── README.md
├── requirements.txt
├── .gitignore
├── .env                 # API keys
├── nim_model_checkingScript.py  # List NIM models
└── Agents/
    ├── simplerag.py     # RAG agent with search/scrape
    ├── tool_calling_agent.py  # Tool calling with web search
    ├── agent_1.py       # Diagnostic agent with fallbacks
    └── HuggingFaceAgent.py  # Party planning with observability
```

</details>

## Installation

1. **Clone the repo**:
   ```
   git clone https://github.com/iamNaman-official/Project-ViperStrike.git
   cd Project-ViperStrike
   ```

2. **Set up virtual environment** (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\\Scripts\\activate  # Windows
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Set up `.env` file** (copy `.env.example` or create manually):
   ```
   GROQ_API_KEY=your_groq_key_here
   NVIDIA_NIM_KEY=your_nvidia_nim_key_here
   # Optional: LANGFUSE_* for observability
   ```
   **Security Note**: Never commit `.env`. Add to `.gitignore`. Get keys from [Groq](https://console.groq.com/keys), [NVIDIA API Catalog](https://build.nvidia.com).

5. **Verify services** (optional):
   ```
   python nim_model_checkingScript.py
   ```

## Quick Start

Run an agent demo:
```bash
# Simple RAG/Search agent
python Agents/simplerag.py

# Tool calling agent
python Agents/tool_calling_agent.py

# Diagnostic fallback demo
python Agents/agent_1.py

# Party planning with tools/observability
python Agents/HuggingFaceAgent.py
```

Expect logs showing service checks, masked keys, and agent outputs.

## Contributing
Fork, PRs welcome! Focus on new agents/tools/frameworks.

## License
MIT License - see [LICENSE](LICENSE) (add if needed).

## Contact
- **GitHub**: [@iamNaman-official](https://github.com/iamNaman-official)
- **LinkedIn**: [Naman Jain](https://www.linkedin.com/in/naman-jain-066b4a262)
