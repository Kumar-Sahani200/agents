from langgraph.graph import StateGraph # type: ignore
from typing import TypedDict, List


# state schema
class AgentState(TypedDict):
    name: str
    operation: str
    numbers: List[int]
    OpeRes: int

# node
def operation_node(state: AgentState) -> AgentState:
    """Node to perform an operation depending on the operation type"""

    if state["operation"] == "+":
        state["OpeRes"] = 0
        state["OpeRes"] = sum(state["numbers"])
    elif state["operation"] == "*":
        state["OpeRes"] = 1
        for num in state["numbers"]:
            state["OpeRes"] *= num

    return state

# define graph
graph = StateGraph(AgentState)

# add node to the graph
graph.add_node("operation", operation_node)

# sandwich the node between entry and exit points
graph.set_entry_point("operation")
graph.set_finish_point("operation")

# compile the graph
app = graph.compile()

# invoke the graph with a message
# and get the result
result = app.invoke({"name": "Kumar", "operation": "*", "numbers": [10, 2, 3]})

# Access the result from the state
resMess = result['OpeRes']

# Output the result of the operation
print(resMess)  
