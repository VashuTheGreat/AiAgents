import asyncio
import logging
import src.logger
from src.graph.builder import graph

async def run_agent():
    logging.info("Starting AIAgents application...")
    # Sample initial state for testing
    config = {"configurable": {"thread_id": "2"}}
    initial_state = {
        "userQuery": "Google ka IPO kis year me hua tha?",
        "db_path": "db/vansh",
        "docs_path": "data/vansh",
        "k": 3
    }
    try:
        response = await graph.ainvoke(initial_state,config=config)
        logging.debug(f"Graph response: {response}")
        logging.info("Graph invocation successful.")
        print("\n--- FINAL LLM RESPONSE ---\n")
        print(response.get("llm_response", "No response found."))
        print("\n--------------------------\n")
    except Exception as e:
        logging.error(f"Application failed: {e}")
        import traceback
        logging.error(traceback.format_exc())
    logging.info("AIAgents application finished.")

if __name__=="__main__":
    asyncio.run(run_agent())