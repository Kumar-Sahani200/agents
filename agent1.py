from langgraph.graph import StateGraph
from typing import Dict, TypedDict


# 1. create a state graph
# 2. define a node
# 3. define a graph and add state and ndoe to it
# 4. define an entry, sandwich the node and define finish point 
# 5. compile the graph
# 5. invoke the graph with a message(key)
# 6. run the graph with the key and get the result



# State Schema
class AgentState(TypedDict):
    message: str

# Node
def node1(state: AgentState) -> AgentState:
    """Simple Node to process the input message and return a compliment"""

    state["message"] = "Hey " + state["message"] + ", you are awesome!"

    return state

# State Graph

graph = StateGraph(AgentState)

# add a node to the graph
graph.add_node("complimenter", node1)

# sandwich the node between entry and exit points
graph.set_entry_point("complimenter")
graph.set_finish_point("complimenter")

# compile the graph
app = graph.compile()

result = app.invoke({"message": "Kumar"})

result = result['message']  # Access the message from the result

print(result)