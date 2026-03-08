import logging
from langgraph.graph import START, END, StateGraph
from src.models.web.web_model import State
from src.nodes.web.webBasedLoader_node import load_web_content
from src.nodes.web.webSummerizer_node import web_summ_node
logging.info("Building web state graph...")
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("load_web_content", load_web_content)
graph_builder.add_node("web_summ_node", web_summ_node)

# Add edges
graph_builder.add_edge(START, "load_web_content")
graph_builder.add_edge("load_web_content", "web_summ_node")
graph_builder.add_edge("web_summ_node", END)

logging.info("Compiling web graph...")
graph = graph_builder.compile()

png_data = graph.get_graph().draw_mermaid_png()
with open("web_graph.png", "wb") as f:
    f.write(png_data)
logging.info("web Graph compiled successfully.")

