from typing import Annotated


from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    flag: bool 


graph_builder = StateGraph(State)



def chatbot(state: State):
    if state["flag"]:
        return {"messages": "It is true!"}
    else:
        return {"messages": "It is false!"}

def chatbot2(state: State):
    return {"messages": "I am a different function!", "flag": False}

def router(state: State):
    if state["flag"]:
        return "chatbot2"
    else:
        return END

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_conditional_edges(
    "chatbot",
    router,
    {"chatbot2": "chatbot2", END: END}
)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot2", chatbot2)
graph_builder.add_edge("chatbot2","chatbot")
graph_builder.set_entry_point("chatbot")
# graph_builder.set_finish_point(END)
graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    initial_state = {
        "messages": [{"role": "user", "content": user_input}],
        "flag": True  # explicitly initialize flag
    }
    for event in graph.stream(initial_state):
        for value in event.values():
            print("Assistant:", value)



#while True:
if __name__ == "__main__":
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            # break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        # break