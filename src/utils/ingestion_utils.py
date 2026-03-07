import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from src.utils.asyncHandler import asyncHandler
from src.constants import EMBEDDING_MODEL
from src.constants import EXCEPTED_FILE_TYPE,RETREIVER_DEFAULT_K
import logging
# import vconsoleprint

# ---------------- Embedding Model ----------------
embedding_model = HuggingFaceEmbeddings(model=EMBEDDING_MODEL)

# ---------------- Document Fetcher ----------------

@asyncHandler
async def document_fetcher(docs: str = "data"):
    """Fetch all files documents from docs folder"""
    logging.info(f"Fetching docs from {docs}")

    if not os.path.exists(docs):
        logging.error(f"Docs folder not found at: {docs}")
        raise FileNotFoundError(f"Docs folder not found at: {docs}")

    logging.info("Scanning for files in ingestion pipeline...")
    files = os.listdir(docs)
    logging.info(f"Files found: {files}")
    
    file_types = [file.split(".")[-1] for file in files]
    unsupported = [f for f, t in zip(files, file_types) if t not in EXCEPTED_FILE_TYPE]
    if unsupported:
        logging.warning(f"Found unsupported file types: {unsupported}")
    
    # Simple TextLoader fallback for txt files to avoid unstructured complexity if not needed
    documents = []
    from langchain_community.document_loaders import TextLoader
    
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(docs, file)
            logging.info(f"Loading text file: {file_path}")
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                documents.extend(loader.load())
            except Exception as e:
                logging.error(f"Failed to load {file_path}: {e}")
        else:
            logging.info(f"Skipping non-txt file: {file}")

    if not documents:
        logging.warning("No documents loaded by TextLoader, trying DirectoryLoader...")
        loader = DirectoryLoader(
            path=docs,
            glob="**/*",
            loader_cls=UnstructuredFileLoader,
            loader_kwargs={"encoding": "utf-8"},
            show_progress=True,
        )
        documents = loader.load()
    
    logging.info(f"Successfully loaded {len(documents)} documents.")
    return documents


# ---------------- Chunking ----------------
@asyncHandler
async def chunking_documents(documents, chunk_size: int = 200, chunk_overlap: int = 0):
    """Split documents into chunks"""
    logging.info("Entered in the chunking documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_documents(documents)
    logging.info("Exiting from the chunking_documents")
    return chunks

@asyncHandler
async def create_vector_store(path: str = "db",docs:str="data"):
    """Create or load Chroma vector database"""

    if os.path.exists(path):
        logging.info("Existing DB found. Loading...")
        vectorstore = Chroma(
            persist_directory=path,
            embedding_function=embedding_model,
            collection_metadata={"hnsw:space": "cosine"},
        )
        return vectorstore

    logging.info("Creating new vector DB...")
    documents = await document_fetcher(docs=docs)
    chunks = await chunking_documents(documents)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=path,
        collection_metadata={"hnsw:space": "cosine"},
    )

    return vectorstore

@asyncHandler
async def create_retreiver(vectorstore, k: int = RETREIVER_DEFAULT_K):
    logging.info(f"Creating retriever with k={k}")
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    logging.info("Retriever created.")
    return retriever







async def get_documents(docs:str="data") -> str:
    documents = await document_fetcher(docs=docs)
    text="\n".join([doc.page_content for doc in documents])
    return text

    
