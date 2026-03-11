import logging
from langgraph.graph import START, END, StateGraph
from src.MultiRag.models.rag_model import State
from src.MultiRag.nodes.retreiver_check_node import retreiver_check
from src.MultiRag.nodes.queries_generator import query_generator
from src.MultiRag.nodes.chat_node import chat
from src.MultiRag.nodes.content_summerizer import content_summerizer
from src.MultiRag.memory import memory
logging.info("Building state graph...")
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("retreiver_check", retreiver_check)
graph_builder.add_node("content_summerizer", content_summerizer)
graph_builder.add_node("qureis_builder", query_generator)
graph_builder.add_node("chat", chat)

# Add edges
graph_builder.add_edge(START, "retreiver_check")
graph_builder.add_edge("retreiver_check", "content_summerizer")
graph_builder.add_edge("content_summerizer", "qureis_builder")
graph_builder.add_edge("qureis_builder", "chat")
graph_builder.add_edge("chat", END)

logging.info("Compiling graph...")
graph = graph_builder.compile(checkpointer=memory)

png_data = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png_data)
logging.info("Graph compiled successfully.")




## ----------- Delete Conversion -----------------
async def deleteThread(thread_id: str):
    try:
        cp = memory
        # Check if thread exists first
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
