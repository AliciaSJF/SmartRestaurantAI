from langgraph.graph import StateGraph, START, END
from src.app.utils.state import State
from src.app.utils.nodes import chatbot_node, human_node, tool_node, order_node

from langgraph.graph import StateGraph, START, END
from src.app.utils.state import State
from src.app.utils.nodes import chatbot_node, tool_node
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

def maybe_route_to_tools(state: State) -> str:
    """
    Decide si ir al tool_node, order_node o finalizar el flujo.
    """
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0:
        for tool_call in last_message.tool_calls:
            # Dirige al nodo de pedidos si es una herramienta de pedidos
            if tool_call["name"] in {"add_to_order", "confirm_order", "get_order", "clear_order", "place_order"}:
                return "order"
        # Caso contrario, dirige al nodo de herramientas estándar
        return "tools"
    return "human"

builder = StateGraph(State)

builder.add_node("chatbot", chatbot_node)
builder.add_node("tools", tool_node)
builder.add_node("human", human_node)
builder.add_node("order", order_node)


builder.add_conditional_edges("chatbot", maybe_route_to_tools)
builder.add_edge("tools", "chatbot") 
builder .add_edge("order", "chatbot")
builder.add_edge(START, "chatbot")    
builder.add_edge("chatbot", END)      

chat_graph = builder.compile(checkpointer=checkpointer)

from IPython.display import Image

mermaid_graph = chat_graph.get_graph().draw_mermaid_png()

image_path = "C:/Users/AliciaSanJuliánFerna/Documents/Python/restaurant-app/graph.png"
with open(image_path, "wb") as file:
    file.write(mermaid_graph)