from langgraph.graph import StateGraph, START, END
from src.MultiRag.models.worker_model import State
from src.MultiRag.nodes.worker import (
    pdf,
    txt,
    docs,
    image,
    url,
    decider
)
from src.MultiRag.constants import AVAILABLE_ANALYSIS
import logging

logging.info("Building worker sub graph")

graph = StateGraph(State)

graph.add_node("decider", decider.decider_node)
graph.add_node("pdf", pdf.pdf_node)
graph.add_node("txt", txt.txt_node)
graph.add_node("docs", docs.docs_node)
graph.add_node("url", url.url_node)
graph.add_node("image", image.image_node)

def route_fn(state: State):
    logging.info(f"Routing based on file_type: {state.file_type}")
    if state.file_type in AVAILABLE_ANALYSIS:
        return state.file_type
    return "end"

graph.add_conditional_edges(
    START,
    route_fn,
    {
        "pdf": "pdf",
        "txt": "txt",
        "docs": "docs",
        "png": "image",
        "url": "url",
        "end":END
    }
)

graph.add_edge("pdf", END)
graph.add_edge("txt", END)
graph.add_edge("docs", END)
graph.add_edge("url", END)
graph.add_edge("image", END)

graph = graph.compile()

try:
    with open("worker_sub_graph.png", "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())
    logging.info("Graph image saved successfully")
except Exception as e:
    logging.error(f"Error saving graph: {e}")
    raise Exception(e)