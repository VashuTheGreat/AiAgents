<div align="center">
  <h1>🤖 AIAgents Platform</h1>
  <p><strong>Intelligent AI Agents Powered by LangGraph, LangChain, and FastAPI</strong></p>
</div>

<br />

Welcome to **AIAgents**, a full-stack, state-of-the-art framework for building and deploying extremely scalable, multi-agent AI ecosystems! Currently featuring powerful autonomous agents for complex Web Research, Document RAG functionality, and interactive multi-turn chatting!

---

## 🚀 Features

- **🌐 Web Research Agent**: Automatically browse, scrape, and synthesize live internet data straight from any URL (including YouTube videos!) directly within the beautiful web interface!
- **📚 Multi-turn RAG Chat**: Chat with arbitrary text or PDF documents using deep LangGraph memory, powerful sentence transformers for vector retrieval, and advanced orchestration logic!
- **🎨 Stunning UI**: Beautiful, fully-responsive, custom Dark Mode interface crafted natively with Jinja2 Templating, vanilla HTML/CSS/JS, glassmorphism UI elements, and snappy fetch-driven loading states.
- **⚡ Supercharged Backend**: High-performance asynchronous API crafted using FastAPI.
- **🛠️ Extensible AI Architecture**: Built on top of the robust **LangChain** and **LangGraph** Python ecosystem to allow infinite scaling of autonomous tool-calling agents.

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, FastAPI, Uvicorn
- **AI Frameworks**: LangChain, LangGraph, Sentence-Transformers, HuggingFace
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

_(This will read `pyproject.toml` and instantly install all your LangChain, FastAPI, and AI dependencies)._

### 2. Environment Variables

Create a `.env` file in the root of the project and place your necessary API keys inside.
Example:

```env
OPENAI_API_KEY="sk-...YOUR_KEY_HERE"
```

### 3. Run the Server

Simply launch the FastAPI application using the built-in server setup:

```bash
uv run .\main.py
```

This will start the development server. Navigate to `http://127.0.0.1:8000/` in your browser to see the beautiful AIAgents Hub!

---

## 🎨 Walkthrough of the Application

### 🏠 Home Page (`/`)

An elegant gateway into the magic. You can navigate directly to the available AI agent interfaces from the dashboard.

### 🌐 Web Summarizer (`/web`)

Paste any website URL or YouTube Link into the URL field! Under the hood, a LangChain WebBaseLoader (or YoutubeLoader) asynchronously extracts the content, checks context lengths, and runs it entirely through the `webSummerizer` node inside our custom LangGraph architecture! The beautiful responsive UI handles rendering the parsed Markdown back to the screen dynamically alongside a spinner loading state.

### 💬 Chat MultiGraph (`/chat`)

Engage with your locally uploaded documents via RAG (Retrieval-Augmented Generation). Our AI uses intelligent memory buffers to recall context gracefully throughout a multi-turn conversation.

---

## 📂 Project Structure

```bash
AiAgents/
├─ api/
│  ├─ routes/         # FastAPI Route definitions (including /web routing)
│  └─ main.py         # App Initialization and Custom Middleware logic
├─ src/
│  ├─ graph/          # LangGraph builders and edges/nodes architecture
│  ├─ llm/            # Core LLM instantiations
│  ├─ models/         # Pydantic & TypedDict Type models for State Management
│  ├─ nodes/          # LLM Nodes, Loaders, Summerizers, and Action Logic
│  ├─ prompts/        # Prompt Templates injected via LangChain
│  └─ utils/          # Custom Exceptions, Wrappers (e.g. @asyncHandler)
├─ static/            # CSS Stylesheets, client-side JS scripts (web.js, chat.js)
├─ templates/         # HTML Jinja2 Views (home.html, base.html, web.html)
└─ pyproject.toml     # uv Dependency file
```

---

<div align="center">
  <p>Crafted with ❤️ for professional creators.</p>
</div>
