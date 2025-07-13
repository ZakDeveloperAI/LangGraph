from  langgraph.graph import StateGraph,END,START
from typing import Dict, TypedDict, Any
import random as rnd
from time import sleep
class State(TypedDict):
    player_name:str
    guesses:list[int]
    attempts:int
    target_number:int | None
    lower_bound:int
    upper_bound:int
    result: str | None
    #next: Any
    
def setup_node(state:State)->State:
    """Setup node"""
    print(f"Hello {state['player_name']} welcome to the guessing game !")
    state["target_number"]=rnd.randint(state["lower_bound"],state["upper_bound"])
    print(f"The random target number is {state['target_number']}")
    print(f"Let's see if the agent can guess it in {state['attempts']} attempts")
    sleep(1)
    return state

def guess_node(state:State)->State:
    """Node that guess the number between two bounds"""
    guessed_number=rnd.randint(state["lower_bound"],state["upper_bound"])
    state["guesses"].append(guessed_number)
    return state
    
def hint_node(state:State)->State:
    """hint node to guide the agent and it also act as a router node"""
    if(state["attempts"]==0):
        state["lower_bound"]=state["guesses"][-1] 
        state["result"]="The agent didn't find the number"
        state["next"]="end"
        return state
    if state["guesses"][-1]==state["target_number"]: 
        state["result"]=f"The agent found the number {state['guesses'][-1]}"
        state["next"]="end"
        return state
    elif state["guesses"][-1]<state["target_number"]: 
        state["lower_bound"]=state["guesses"][-1] +1
        state["next"]="guess"
        state["attempts"]=state["attempts"]-1
    elif state["guesses"][-1]>state["target_number"]: 
        state["upper_bound"]=state["guesses"][-1] -1
        state["next"]="guess"
        state["attempts"]=state["attempts"]-1
    return state

graph_builder=StateGraph(State)

graph_builder.add_node("setup",setup_node)
graph_builder.add_node("guess",guess_node)
graph_builder.add_node("hint",hint_node)

graph_builder.add_edge(START,"setup")
graph_builder.add_edge("setup","guess")
graph_builder.add_edge("guess","hint")
graph_builder.add_conditional_edges(
    "hint",
    lambda state:state.get("next"),
    {"guess":"guess","end":END}
)

graph=graph_builder.compile()
initial_state=State(player_name="Zak",lower_bound=1,upper_bound=40,guesses=[],attempts=7)
final_state=graph.invoke(initial_state)
print(final_state["guesses"])
print(final_state["result"])