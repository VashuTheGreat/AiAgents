import logging
from src.MultiRag.models.rag_model import State
from utils.asyncHandler import asyncHandler
from src.MultiRag.entity.ingestion_config import IngestionConfig
from src.MultiRag.ingestion.ingest_pipeline import Ingestion
from src.MultiRag.retrievers.retriever import Retreiver
import os

# ─────────────────────────────────────────────────────────────────────────────
# Server-side in-memory retriever cache.
# Keyed by db_path so each user gets their own isolated retriever instance.
# This avoids storing non-serializable objects in LangGraph state
# while still preserving per-user retriever isolation across requests.
# ─────────────────────────────────────────────────────────────────────────────
_RETRIEVER_CACHE: dict[str, Retreiver] = {}


@asyncHandler
async def retreiver_check(state: State):
    """
    Ensures a retriever exists for the current user (keyed by db_path).
    - If cached → reuses existing instance (fast).
    - If not cached → runs ingestion + creates retriever, then caches it.
    The retriever is NOT stored in state (not msgpack-serializable).
    Instead it lives in _RETRIEVER_CACHE, accessible by db_path.
    """
    db_path = state['db_path']
    docs_path = state['docs_path']

    if db_path in _RETRIEVER_CACHE:
        logging.info(f"Retriever cache hit for db_path={db_path}")
        return {}

    logging.info(f"Retriever cache miss for db_path={db_path}. Initializing...")

    if not os.path.exists(docs_path):
        logging.info(f"Creating documents directory: {docs_path}")
        os.makedirs(docs_path, exist_ok=True)

    ingestion_config = IngestionConfig(db_path=db_path, docs_path=docs_path)
    logging.info("Starting ingestion pipeline...")
    ingestion = Ingestion(ingestion_config=ingestion_config)
    ingestion_artifact = await ingestion.ingest_data()

    logging.info("Initializing retriever with ingestion artifacts...")
    retreiver = Retreiver(vector_db=ingestion_artifact.vector_db, k=state['k'])
    await retreiver.initiate_retreiver()

    _RETRIEVER_CACHE[db_path] = retreiver
    logging.info(f"Retriever cached for db_path={db_path}.")
    return {}


def get_cached_retriever(db_path: str) -> Retreiver | None:
    """Helper used by downstream nodes to fetch the retriever by db_path."""
    return _RETRIEVER_CACHE.get(db_path)


def clear_cached_retriever(db_path: str) -> None:
    """
    Release Chroma file handles for the given db_path before shutil.rmtree.

    CRITICAL ORDER on Windows (HNSW data_level0.bin is memory-mapped):
      1. Stop the specific chromadb _system WHILE the Python object is alive
         → this unmaps the HNSW index (releases data_level0.bin OS handle)
      2. Null Python references
      3. gc.collect() — free remaining CPython objects
      4. clear_system_cache() — clean up the global chromadb registry
    """
    import gc
    import chromadb

    retriever = _RETRIEVER_CACHE.pop(db_path, None)

    if retriever is not None:
        # Step 1: Stop the SPECIFIC chroma system while Python obj is still alive.
        # This calls HnswSegment.stop() → hnswlib.Index.close() → munmap().
        # Must happen BEFORE nulling vector_db, or the system ref is gone.
        try:
            vdb = retriever.vector_db
            if vdb is not None and hasattr(vdb, '_client'):
                client = vdb._client
                # PersistentClient / SharedSystemClient stores system in _system
                if hasattr(client, '_system') and client._system is not None:
                    client._system.stop()
                    logging.info(f"Chromadb _system stopped for db_path={db_path}")
        except Exception as e:
            logging.warning(f"Could not stop chromadb _system: {e}")

        # Step 2: Null all Python references
        retriever.retreiver = None
        retriever.vector_db = None
        logging.info(f"Retriever refs nulled for db_path={db_path}")

    # Step 3: Free objects immediately
    gc.collect()

    # Step 4: Clean up chromadb's global system registry
    try:
        chromadb.api.client.SharedSystemClient.clear_system_cache()
        logging.info("Chromadb global system cache cleared.")
    except Exception as e:
        logging.warning(f"Could not clear chromadb system cache: {e}")
