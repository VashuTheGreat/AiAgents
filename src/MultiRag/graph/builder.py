import logging
from langgraph.graph import START, END, StateGraph
from src.MultiRag.models.rag_model import State
from src.MultiRag.nodes.chat_node import chat_node
from src.MultiRag.graph.worker.builder import graph as worker_sub_graph
from src.MultiRag.nodes.orchestrator_node import orchestrator_node
from src.MultiRag.nodes.reducer_node import reducer_node
from src.MultiRag.memory import memory
from langgraph.types import Send

logging.info("Initializing StateGraph with State model...")
graph_builder = StateGraph(State)

def fanout(state: State):
    logging.info("Evaluating fanout condition from orchestrator_node")
    
    plan = state.get("plan")
    if not plan:
        logging.warning("No plan found in state, defaulting to chat_node")
        return "chat_node"
    
    if not plan.use_worker:
        logging.info("Orchestrator decided to bypass workers and go to chat")
        return "chat_node"

    tasks = plan.tasks or []
    if not tasks:
        logging.info("No tasks to execute, going to chat_node")
        return "chat_node"

    logging.info(f"Fanning out {len(tasks)} tasks to workers")
    
    return [
        Send(
            "worker",
            {
                "plan_to_retrieve": task.instruction,
                "file_type": task.file_type,
                "file_path": task.file_path,
                "analysis_result": None,
            },
        )
        for task in tasks
    ]

logging.info("Adding nodes to graph builder: orchestrator_node, chat_node, worker, reducer_node")
graph_builder.add_node("orchestrator_node", orchestrator_node)
graph_builder.add_node("chat_node", chat_node)
graph_builder.add_node("worker", worker_sub_graph)
graph_builder.add_node("reducer_node", reducer_node)

logging.info("Configuring graph edges and flow...")
graph_builder.add_edge(START, "orchestrator_node")

logging.info("Setting up conditional edges from orchestrator_node using fanout")
graph_builder.add_conditional_edges(
    "orchestrator_node", 
    fanout, 
    {
        "worker": "worker",
        "chat_node": "chat_node"
    }
)

logging.info("Connecting worker to reducer_node and then to chat_node")
graph_builder.add_edge("worker", "reducer_node")
graph_builder.add_edge("reducer_node", "chat_node")
graph_builder.add_edge("chat_node", END)

logging.info("Compiling graph...")
graph = graph_builder.compile(checkpointer=memory)

try:
    png_data = graph.get_graph(xray=1).draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png_data)
    logging.info("Graph visualization saved to graph.png")
except Exception as e:
    logging.warning(f"Could not generate graph visualization: {e}")

logging.info("Graph compiled successfully.")

async def deleteThread(thread_id: str):
    try:
        cp = memory
        state = await cp.aget_tuple(config={'configurable': {'thread_id': thread_id}})
        if state is None:
            logging.info(f"Thread {thread_id} not found, nothing to delete.")
            return False
            
        await cp.adelete_thread(thread_id=thread_id)
        logging.info(f"Thread {thread_id} deleted successfully.")
        return True
    except Exception as e:
        logging.error(f"Error deleting thread {thread_id}: {e}")
        return False
