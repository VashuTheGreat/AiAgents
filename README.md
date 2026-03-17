

---
title: Multi-Rag AI
emoji: ⚖️
colorFrom: blue
colorTo: green
sdk: docker
app_file: Dockerfile
app_port: 7860
pinned: false
---


<div align="center">
  <h1>🤖 AIAgents Platform</h1>
  <p><strong>Intelligent AI Agents Powered by LangGraph, LangChain, and FastAPI</strong></p>
</div>

<br />

Welcome to **AIAgents**, a full-stack, state-of-the-art framework for building and deploying extremely scalable, multi-agent AI ecosystems! Featuring powerful autonomous agents for complex Web Research, Blog Generation, Document RAG functionality, and interactive multi-turn chatting!

---

## 🚀 Features

- **✍️ Bloggig (Blog Agent)**: Powerful autonomous agent that researches, writes, and generates high-quality blog posts complete with AI-generated visuals.
- **🌐 Web Research Agent**: Automatically browse, scrape, and synthesize live internet data straight from any URL (including YouTube videos!) directly within the web interface.
- **📚 Multi-turn RAG Chat**: Chat with arbitrary text or PDF documents using deep LangGraph memory, powerful sentence transformers for vector retrieval, and advanced orchestration logic.
- **🎨 Stunning UI**: Beautiful, fully-responsive, custom Dark Mode interface crafted natively with Jinja2 Templating, vanilla HTML/CSS/JS, and glassmorphism UI elements.
- **⚡ Supercharged Backend**: High-performance asynchronous API crafted using FastAPI.
- **🛠️ Extensible AI Architecture**: Built on top of the robust **LangChain** and **LangGraph** Python ecosystem to allow autonomous scaling of multi-agent workflows.

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, FastAPI, Uvicorn
- **AI Frameworks**: LangChain, LangGraph, Sentence-Transformers, HuggingFace
- **LLMs**: AWS Bedrock (Claude 3.5 Sonnet, Claude 3 Haiku, Llama 3), OpenAI (GPT-4o)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Frontend**: Jinja2 Templates, Vanilla JS, CSS3, DOM manipulation
- **Development Tooling**: `uv` (Fast Python Package Manager)

---

## ⚙️ Quickstart

### Prerequisites

- Ensure you have **Python >= 3.12** installed on your system.
- Make sure you are using [uv](https://github.com/astral-sh/uv) to manage project dependencies!

### 1. Installation

1. **Clone the repository**:
```bash
git clone https://github.com/VashuTheGreat/AiAgents.git
cd AiAgents
```

2. **Set up the virtual environment & install dependencies** using `uv`:
```bash
uv sync
```

### 2. Environment Variables

Create a `.env` file in the root of the project and place your necessary API keys inside.

```env
# General
APP_API_KEY="your_custom_auth_key"

# AWS Bedrock (For Blog Agent)
AWS_ACCESS_KEY_ID="your_key"
AWS_SECRET_ACCESS_KEY="your_secret"
AWS_REGION_NAME="us-east-1"

# OpenAI
OPENAI_API_KEY="sk-..."
```

### 3. Run the Server

Simply launch the FastAPI application:
```bash
uv run .\main.py
```
This will start the development server. Navigate to `http://127.0.0.1:8000/` to see the AIAgents Hub!

---

## 🎨 Walkthrough of the Application

### 🏠 Home Page (`/`)
An elegant gateway into the available AI agent interfaces.

### ✍️ Blog Agent (`/blog`)
The flagship feature. Enter a topic, and Bloggig will autonomously research the subject, plan its structure, write the content in Markdown, and generate relevant images. It features a real-time "pipeline console" to track the agent's progress.

### 🌐 Web Summarizer (`/web`)
Paste any URL or YouTube Link to extract and summarize content using our custom LangGraph architecture.

### 💬 Chat MultiGraph (`/chat`)
Engage with your locally uploaded documents via RAG (Retrieval-Augmented Generation) with intelligent memory buffers.

---

## 📂 Project Structure

```bash
AiAgents/
├─ api/
│  ├─ Blog/           # Bloggig-specific routers and models
│  ├─ MultiRag/       # Document RAG routers
│  └─ Web/            # Web Summarizer routers
├─ src/
│  ├─ Blog/           # Bloggig Agent logic (Graph, Nodes, Prompts)
│  ├─ MultiRag/       # RAG Agent logic (Retrievers, Vectorstores, etc.)
│  └─ Web/            # Web Agent logic (Loaders, Graph)
├─ images/            # Generated blog visualizations
├─ results/           # Saved blog markdown outputs
├─ static/            # CSS, JS, and local frontend assets
├─ templates/         # Jinja2 HTML templates
├─ data/              # Raw document storage for RAG
├─ db/                # Local FAISS vector database storage
└─ pyproject.toml     # Project dependencies (uv)
```

---

<div align="center">
  <p>Crafted with ❤️ for professional creators.</p>
</div>
