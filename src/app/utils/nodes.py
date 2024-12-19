from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from src.app.utils.state import State
from langgraph.types import interrupt, Command
from .tools import  create_reservation
from langgraph.graph import StateGraph, START, END
from src.app.utils.prompts import SYSTEM_PROMPT,WELCOME_MESSAGE
from langchain.schema import HumanMessage, AIMessage
from langchain_core import tools
from src.app.utils.tools import get_menu, get_menu_with_ingredients, get_menu_item, create_reservation, add_to_order, confirm_order, place_order,clear_order
from langgraph.prebuilt import ToolNode
from langchain_core.messages.tool import ToolMessage


import logging


logger = logging.getLogger(__name__)

# Configurar el modelo de OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9)
tools = [get_menu,get_menu_with_ingredients,get_menu_item,add_to_order,confirm_order,place_order,clear_order]
menu_tools = [get_menu,get_menu_with_ingredients,get_menu_item]
order_tools = [add_to_order,confirm_order,place_order,clear_order]
llm_with_tools = llm.bind_tools(tools)


# Nodo de herramientas: ejecuta herramientas solicitadas
tool_node = ToolNode(tools)


# Nodo humano: recibe mensajes del usuario
def human_node(state: State) -> State:
    """
    Nodo que recibe el input del usuario.
    """
    return state  # Devuelve el estado tal como está

def chatbot_node(state: State) -> State:
    logger.info("chatbot_node")
    """
    Nodo principal del chatbot: invoca el LLM y detecta tool_calls.
    """
    defaults = { "order": [] , "finished": False }
    if not state.get("messages"):
        response = llm_with_tools.invoke([AIMessage(content=WELCOME_MESSAGE)])
    else:
        messages = state["messages"]
        response = llm_with_tools.invoke([AIMessage(content=SYSTEM_PROMPT)] + messages)
    return {"messages": state.get("messages", []) + [response], **defaults}


def order_node(state: State) -> State:
    logger.info("order_node")
    """Manipula el pedido actual, incluida la confirmación."""
    tool_msg = state["messages"][-1]  # Último mensaje con tool_calls
    order = state.get("current_order", [])
    outbound_msgs = []

    for tool_call in tool_msg.tool_calls:
        tool_name = tool_call["name"]

        if tool_name == "add_to_order":
            logger.info(f"add_to_order: {tool_call}")
            dish = tool_call["args"]["dish"]
            quantity = tool_call["args"]["quantity"]
            order.append(f"{quantity} x {dish}")
            logger.info(f"Pedido actual: {order}")
            response = f"Se añadió {quantity} x {dish} al pedido."

        elif tool_name == "get_order":
            logger.info(f"get_order: {tool_call}")
            response = "\n".join(order) if order else "El pedido está vacío."

        elif tool_name == "clear_order":
            logger.info(f"clear_order: {tool_call}")
            order.clear()
            response = "El pedido ha sido eliminado."

        elif tool_name == "confirm_order":
            logger.info(f"confirm_order: {tool_call}")
            response = f"Tu pedido actual es:\n{'\n'.join(order)}\n¿Es correcto?"

        elif tool_name == "place_order":
            logger.info(f"place_order: {tool_call}")
            response = "Pedido enviado a la cocina. Estará listo en 15 minutos."
            state["finished"] = True

        else:
            raise NotImplementedError(f"Herramienta desconocida: {tool_name}")

        # Generar un tool_message para cada tool_call
        outbound_msgs.append(
            ToolMessage(
                content=response,
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )

    # Devolver los mensajes generados y actualizar el estado del pedido
    return {"messages": outbound_msgs, "current_order": order, "finished": state.get("finished", False)}