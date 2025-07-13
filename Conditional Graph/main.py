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
    if state['operation1']=="-": return {"next":"substract"}
    elif state['operation1']=="+": return {"next":"add"}
    else: raise ValueError("operation not supported")
    
def add_node(state:State)->State:
    """node that adds two given numbers"""
    state["result1"]=state["number1"]+state["number2"]
    return state

def substract_node(state:State)->State:
    """node that adds two given numbers"""
    state["result1"]=state["number1"]-state["number2"]
    return state

def router_node2(state:State)->State:
    """node that Routes to the next node"""
    if state['operation2']=="-": return {"next":"substract2"}
    elif state['operation2']=="+": return {"next":"add2"}
    else: raise ValueError("operation not supported")
    
def add_node2(state:State)->State:
    """node that adds two given numbers"""
    state["result2"]=state["number3"]+state["number4"]
    return state

def substract_node2(state:State)->State:
    """node that adds two given numbers"""
    state["result2"]=state["number3"]-state["number4"]
    return state

graph_builder=StateGraph(State)

graph_builder.add_node("router",router_node)
graph_builder.add_node("add",add_node)
graph_builder.add_node("substract",substract_node)
graph_builder.add_node("router2",router_node2)
graph_builder.add_node("add2",add_node2)
graph_builder.add_node("substract2",substract_node2)


graph_builder.add_edge(START,"router")

graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {"add": "add","substract": "substract"}
)

graph_builder.add_edge("add","router2")
graph_builder.add_edge("substract","router2")

graph_builder.add_conditional_edges(
    "router2",
    lambda state: state.get("next"), #important
    {"add2": "add2","substract2": "substract2"}
)

graph_builder.add_edge("add2",END)
graph_builder.add_edge("substract2",END)


graph=graph_builder.compile()

initial_state=State(
    number1=10,number2=5,operation1="-",number3=7,number4=2,operation2="+"
)

final_state=graph.invoke(initial_state)
print(final_state["result2"])
