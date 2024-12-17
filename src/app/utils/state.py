from typing import Annotated, List

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage



class State(TypedDict):

    """
    Estado del grafo: historial de mensajes.
    """
    messages: Annotated[List[BaseMessage], add_messages]


