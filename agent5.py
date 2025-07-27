from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
import random

# State Schema
class AgentState(TypedDict):
    name: str
    guesses: List[int]
    lowerBound: int
    upperBound: int
    maxAttempts: int
    ans: int


# Nodes
def greeting_node(state: AgentState) -> AgentState:
    """This node greets the user"""
    state["name"] = f"Hello {state['name']}!"

    print(state["name"])

    return state

def guess_node(state: AgentState) -> AgentState:
    """This node gusses a number betweeen lowerBound and upperBound"""

    random_guess = random.randint(state['lowerBound'], state['upperBound'])

    state['guesses'].append(random_guess)
    state['maxAttempts'] -= 1

    print(f"Random guess: {random_guess}")
    print(f"Remaining attempts: {state['maxAttempts']}")

    return state


def hint_node(state: AgentState) -> AgentState:
    """This node validates and provides a hint based on the last guess"""

    if state['maxAttempts'] <= 0:
        print("No more attempts left!")
        return "edge_exit"

    lastGuess = state['guesses'][-1]

    if lastGuess < state['ans']:
        print("Hint: The number is higher than your last guess.")
        return "edge_guess_again"
    elif lastGuess > state['ans']:
        print("Hint: The number is lower than your last guess.")
        return "edge_guess_again"
    else:
        print("Congratulations! You've guessed the number!")
        return "edge_exit"
    

def exit_node(state: AgentState) -> AgentState:
    """This node exits the game"""
    print("Exiting the game. Thanks for playing!")
    return state

graph = StateGraph(AgentState)

# Adding nodes to the graph
graph.add_node("greeting_node", greeting_node)
graph.add_node("guess_node", guess_node)
graph.add_node("hint_node", lambda state: state)
graph.add_node("exit_node", exit_node)

# Setting up the graph structure
graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node", "guess_node")
graph.add_edge("guess_node", "hint_node")
graph.add_edge("exit_node", END)

graph.add_conditional_edges("hint_node", hint_node, {
    "edge_guess_again": "guess_node",
    "edge_exit": "exit_node"
})


app = graph.compile()

initial_state = AgentState(name="Kumar", guesses=[], lowerBound=1, upperBound=20, maxAttempts=7, ans=5)        

result = app.invoke(initial_state)

print(result)