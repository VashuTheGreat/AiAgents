import logging
from langgraph.graph import StateGraph,START,END
from src.Blog.models.ImageSpec_model import State
from src.Blog.graph.nodes.reducer_sub_node import reducer_sub_image,reducer_sub_llm,merge_images_and_md
app=StateGraph(State)


app.add_node("reducer_sub_llm",reducer_sub_llm)
app.add_node("reducer_sub_image",reducer_sub_image)
app.add_node("merge_images_and_md",merge_images_and_md)

app.add_edge(START,"reducer_sub_llm")
app.add_edge("reducer_sub_llm","reducer_sub_image")
app.add_edge("reducer_sub_image","merge_images_and_md")
app.add_edge("merge_images_and_md",END)




app=app.compile()
logging.info("Reducer subgraph compiled successfully")

