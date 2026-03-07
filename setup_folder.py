import os

PROJECT_NAME = "."

folders = [
    "src/ingestion",
    "src/chunking",
    "src/embeddings",
    "src/vectorstore",
    "src/retrievers",
    "src/chains",
    "src/prompts",
    "src/llm",
    "src/evaluation",
    "src/utils",
    "src/config",

    "api",
    "data/raw",
    "data/processed",
    "vector_db",
    "experiments",
    "monitoring",
    "notebooks",
    "tests",

    "deployment",
    "configs"
]

files = {
    "src/ingestion/ingest_pipeline.py": "",
    "src/chunking/text_chunker.py": "",
    "src/embeddings/embedding_model.py": "",
    "src/vectorstore/vector_db.py": "",
    "src/retrievers/retriever.py": "",
    "src/chains/rag_chain.py": "",
    "src/prompts/prompt_templates.py": "",
    "src/llm/llm_loader.py": "",
    "src/evaluation/rag_metrics.py": "",
    "src/utils/helpers.py": "",
    "src/config/settings.py": "",

    "api/routes.py": "",
    "api/main.py": "",

    "deployment/Dockerfile": "",
    "deployment/docker-compose.yml": "",

    "configs/rag_config.yaml": "",

    ".env": "",
    "requirements.txt": "",
    "README.md": ""
}

# Create project root
os.makedirs(PROJECT_NAME, exist_ok=True)

# Create folders
for folder in folders:
    path = os.path.join(PROJECT_NAME, folder)
    os.makedirs(path, exist_ok=True)

# Create files
for file_path, content in files.items():
    full_path = os.path.join(PROJECT_NAME, file_path)
    with open(full_path, "w") as f:
        f.write(content)

print(f"✅ RAG LLMOps project '{PROJECT_NAME}' created successfully!")