from langgraph.graph import StateGraph, START, END  # type: ignore
from typing import TypedDict

# State Schema
class AgentState(TypedDict):
    num1: int
    num2: int
    opr1: str
    num3: int
    num4: int
    opr2: str
    res1: int
    res2: int

# Nodes for num1 and num2 operations
def addOrSubNum1Num2(state: AgentState) -> AgentState:
    """This node decides which operation to perform on num1 and num2."""
    if state['opr1'] == '+':
        return "edge_num1_add_num2"
    elif state['opr1'] == '-':
        return "edge_num1_sub_num2"
    
def num1_add_num2(state: AgentState) -> AgentState:
    """This node adds num1 and num2 and stores the result in res1."""
    state["res1"] = state["num1"] + state["num2"]
    return state

def num1_sub_num2(state: AgentState) -> AgentState:
    """This node subtracts num3 and num4 and stores the result in res2."""
    state["res1"] = state["num1"] - state["num2"]
    return state


# nodes for num3 and num4 operations
def addOrSubNum3Num4(state: AgentState) -> AgentState:
    """This node decides which operation to perform on num3 and num4."""
    if state['opr2'] == '+':
        return "edge_num3_add_num4"
    elif state['opr2'] == '-':
        return "edge_num3_sub_num4"

def num3_add_num4(state: AgentState) -> AgentState:
    """This node adds num3 and num4 and stores the result in res2."""
    state["res2"] = state["num3"] + state["num4"]
    return state

def num3_sub_num4(state: AgentState) -> AgentState:
    """This node subtracts num3 and num4 and stores the result in res2."""
    state["res2"] = state["num3"] - state["num4"]
    return state


# State Graph
graph = StateGraph(AgentState)

graph.add_node("num1_add_num2", num1_add_num2)
graph.add_node("num1_sub_num2", num1_sub_num2)
graph.add_node("router1", lambda state: state)
graph.add_node("num3_add_num4", num3_add_num4)
graph.add_node("num3_sub_num4", num3_sub_num4)
graph.add_node("router2", lambda state: state)

graph.add_edge(START, "router1")

graph.add_conditional_edges("router1", addOrSubNum1Num2, {
    "edge_num1_add_num2": "num1_add_num2",
    "edge_num1_sub_num2": "num1_sub_num2"
})

graph.add_edge("num1_add_num2", "router2")
graph.add_edge("num1_sub_num2", "router2")

graph.add_conditional_edges("router2", addOrSubNum3Num4, {
    "edge_num3_add_num4": "num3_add_num4",
    "edge_num3_sub_num4": "num3_sub_num4"
})

graph.add_edge("num3_add_num4", END)
graph.add_edge("num3_sub_num4", END)

app = graph.compile()


intial_state = AgentState(num1=10, num2=5, opr1='+', num3=20, num4=10, opr2='-', res1=0, res2=0)

result1 = app.invoke(intial_state)
print(result1)


