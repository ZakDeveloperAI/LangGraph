from langgraph.graph import StateGraph, START, END
from typing import Dict, TypedDict

class State(TypedDict):
    name:str
    age:int
    skills:list[str]
    message:str | None
    
def greet_node(state: State) -> State:
    """A node that greets the user based only by their name"""
    state['message'] = f"Hello, {state['name']}!"
    return state

def age_node(state: State) -> State:
    """A node that adds the user's age to their message"""
    state['message'] += f" You are {state['age']} years old."
    return state

def skills_node(state: State) -> State:
    """A node that lists the user's skills in their message"""
    state['message'] += " You have the following skills:"
    for skill in state['skills']:
        if state["skills"].index(skill)==len(state["skills"])-1:
            state['message'] += f" {skill}"
        else:
            state['message'] += f" {skill},"
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("greetings",greet_node)
graph_builder.add_node("age",age_node)
graph_builder.add_node("skills",skills_node)

graph_builder.add_edge(START,"greetings")
graph_builder.add_edge("greetings","age")
graph_builder.add_edge("age","skills")
graph_builder.add_edge("skills",END)

graph=graph_builder.compile()

init_state=State(name="Zak",age="99",skills=["AI","ML","Computer Vision"])
final_state=graph.invoke(init_state)

print(final_state["message"])