from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from src.app.utils.state import State
from .tools import get_menu_items, create_reservation
from langgraph.graph import StateGraph, START, END
from langchain.schema import HumanMessage, AIMessage
from langchain_core import tools
from src.app.utils.tools import get_menu
from src.app.utils.prompts import SYSTEM_PROMPT, WELCOME_MESSAGE
from langgraph.prebuilt import ToolNode


# Configurar el modelo de OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
llm_with_tools = llm.bind_tools([get_menu])

tools = [
    {"name": "get_menu", "description": "Devuelve el menú actual del restaurante."}
]

def build_tools_prompt(tools):
    """
    Crea un mensaje con el listado de herramientas disponibles.
    """
    prompt = "Las herramientas disponibles son:\n"
    for tool in tools:
        prompt += f"- {tool['name']}: {tool['description']}\n"
    return prompt

tools_prompt = build_tools_prompt(tools)


# Nodo humano: recibe mensajes del usuario
def human_node(state: State) -> State:
    """
    Nodo que recibe el input del usuario.
    """
    return state  # Devuelve el estado tal como está

def chatbot_node(state: State) -> State:
    """
    Nodo principal del chatbot: invoca el LLM y detecta tool_calls.
    """
    messages = state["messages"]

    # Agregar el prompt del sistema
    system_message = AIMessage(content=SYSTEM_PROMPT)

    # Invocar el modelo con herramientas asociadas
    response = llm_with_tools.invoke([system_message] + messages)

    # Actualizar el historial de mensajes con la respuesta
    return {"messages": messages + [response]}

# Nodo de herramientas: ejecuta herramientas solicitadas
tool_node = ToolNode([get_menu])


# def chatbot(state: State) -> State:
#     """
#     Nodo que recibe el historial de mensajes y añade la respuesta del modelo.
#     """
#     # Invoca el modelo con el historial de mensajes
#     response = llm.invoke(state["messages"])
    
#     # Devuelve el estado actualizado con la respuesta del modelo
#     return {"messages": state["messages"] + [AIMessage(content=response.content)]}
 
def menu_response(state: State) -> State:
    """
    Nodo para responder preguntas sobre el menú usando la base de datos.
    """
    menu = get_menu_items()
    return {"messages": state["messages"] + [AIMessage(content=menu)]}

# def general_response(state: AgentState) -> AgentState:
#     """Nodo para responder preguntas generales."""
#     prompt = f"Eres un asistente del restaurante. Pregunta del usuario: {state['query']}"
#     response = model([HumanMessage(content=prompt)])
    
#     state["response"] = response.content  # Actualiza la respuesta
#     state["messages"].append(HumanMessage(content=prompt))  # Agrega al historial
#     return state

# def menu_lookup(state: AgentState) -> AgentState:
#     """Nodo para devolver el menú."""
#     menu = get_menu_items()
    
#     state["response"] = menu  # Actualiza la respuesta
#     state["messages"].append(HumanMessage(content=menu))  # Agrega al historial
#     return state

# def make_reservation(state: AgentState) -> AgentState:
#     """Nodo para crear una reserva."""
#     confirmation = create_reservation(name="Cliente Genérico", guests=2)
    
#     state["response"] = confirmation  # Actualiza la respuesta
#     state["messages"].append(HumanMessage(content=confirmation))  # Agrega al historial
#     return state

