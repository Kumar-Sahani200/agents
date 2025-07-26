from langgraph.graph import StateGraph #type: ignore
from typing import TypedDict

# State Schema
class AgentState(TypedDict):
    name: str
    age: str
    skills: str
    res: str

# Nodes
def node1(state: AgentState) -> AgentState:
    """This node processes the input state and concatenates name in the result with a greeting"""

    state["res"] = f"hello {state['name']}"

    return state

def node2(state: AgentState) -> AgentState:
    """This node processes the input state and concatenates age with the result"""

    state["res"] += f" You are {state['age']} years old."

    return state


def node3(state: AgentState) -> AgentState:
    """This node processes the input state and concatenates skills with the result"""
    
    state["res"] += f" Your skills are: {state['skills']}."

    return state


# State Graph
graph = StateGraph(AgentState)

graph.add_node("node1", node1)
graph.add_node("node2", node2)
graph.add_node("node3", node3)

graph.set_entry_point('node1')
graph.add_edge('node1', 'node2')
graph.add_edge('node2', 'node3')
graph.set_finish_point('node3')

app = graph.compile()

result = app.invoke({"name": "Kumar", "age": "30", "skills": "Python, AI"})

print(result['res'])  # Access the result from the state

