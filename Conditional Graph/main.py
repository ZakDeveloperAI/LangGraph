from langgraph.graph import StateGraph,END,START
from typing import Dict, TypedDict

class State(TypedDict):
    number1:int
    number2:int
    number3:int
    number4:int
    operation1:str
    operation2:str
    result1:int | None
    result2:int | None
    
def router_node(state:State)->State:
    """node that Routes to the next node"""
    if state['operation1']=="-": return {"next":"diff"}
    elif state['operation1']=="+": return {"next":"sum"}
    else: raise ValueError("operation not supported")



graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {"therapist": "therapist","logical": "logical","dan":"dan"}
)
