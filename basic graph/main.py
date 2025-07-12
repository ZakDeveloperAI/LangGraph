from typing import Dict, TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message: str

def greeting_node(state: State) -> State:
    """A node that returns a greeting message."""
    state["message"] = f"Hello {state['message']}, welcome to the graph!"
    print(state["message"])
    return state

graph_builder=StateGraph(State)


graph_builder.add_node("greeting", greeting_node)

graph_builder.add_edge(START, "greeting")
graph_builder.add_edge("greeting", END)

graph=graph_builder.compile()

state={"message": "Alice"}

graph.invoke(state)