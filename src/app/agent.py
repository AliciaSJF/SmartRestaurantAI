from langgraph.graph import StateGraph, START, END
from src.app.utils.state import State
from src.app.utils.nodes import chatbot_node, human_node, tool_node

from langgraph.graph import StateGraph, START, END
from src.app.utils.state import State
from src.app.utils.nodes import chatbot_node, tool_node

def maybe_route_to_tools(state: State) -> str:
    """
    Decide si ir al tool_node o finalizar el flujo.
    """
    last_message = state["messages"][-1]

    # Si hay tool_calls, dirigir al nodo tools
    if hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0:
        return "tools"
    return "human"

builder = StateGraph(State)

builder.add_node("chatbot", chatbot_node)
builder.add_node("tools", tool_node)
builder.add_node("human", human_node)

builder.add_conditional_edges("chatbot", maybe_route_to_tools)
builder.add_edge("tools", "chatbot") 
builder.add_edge(START, "chatbot")    
builder.add_edge("chatbot", END)      

chat_graph = builder.compile()
