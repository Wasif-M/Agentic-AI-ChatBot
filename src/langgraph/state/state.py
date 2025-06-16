from typing import TypedDict,Annotated,List
from langgraph.graph.message import add_messages


class State(TypedDict):
    """
    Reprsent the structure of the state use in graph
    """
    messages: Annotated[str,add_messages]