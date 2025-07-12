from langgraph.graph import StateGraph, START, END
from typing import Dict, TypedDict

class State(TypedDict):
    name: str
    values: list
    operation: str
    result: float | None
    
def calculate_node(state: State) -> State:
    """A node that performs a calculation given by the user"""
    if state["operation"] == "+":
        res=sum([n for n in state["values"]])
    elif state["operation"] == "*":
        res=1
        for n in state["values"]:
            res*=n
    else:
        res=None
        raise ValueError("Unsupported operation")
        
    state["result"] = res
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("calculate", calculate_node)

graph_builder.add_edge(START, "calculate")
graph_builder.add_edge("calculate", END)

graph = graph_builder.compile()

state= State(name="Alice", values=[1, 2, 4], operation="*")
final_state=graph.invoke(state)

print(final_state["result"]) 