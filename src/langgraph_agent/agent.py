import datetime
from functools import partial

import httpx
import langgraph
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.graph import END, START, MessagesState, StateGraph

server_url = "http://localhost:9090/v1/chat/completions"

system_prompt = "You are an assistant model. Give the answer to user's query."

agent_conversations = []


def mock_llm(state: MessagesState):
    messages = state["messages"]

    formatted_messages = [
        {"role": "system", "content": system_prompt},
    ]
    for user_message in messages:
        formatted_messages.append({"role": "user", "content": user_message.content})

    data = {
        "model": "google/gemma-2b",
        "messages": formatted_messages,
        "max_tokens": 50,  # 1. LIMIT tokens so it doesn't run forever
        "temperature": 0.5,
        "stop": [
            "<|im_end|>",
            "<end_of_turn>",
            "user\n",
            "assistant\n",
            "<|im_start|>",
        ],
    }

    response = httpx.post(server_url, json=data, timeout=300)

    chat_result = response.json()["choices"][0]["message"]["content"]

    return {"messages": [AIMessage(content=chat_result)]}


def get_current_timestamp(state: MessagesState):
    """
    This function is a tool for agent to fetch the current timestamp.
    This return string formatted current timestamp in IST.
    """
    return {
        "messages": ToolMessage(
            content="I am sharing important information that can help you decide. The current timestamp is : "
            + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            tool_call_id="current_timestamp",
        )
    }


def store_agent_conversations(state: MessagesState):
    if state["messages"]:
        for message in state["messages"]:
            agent_conversations.append(f"{message.type.upper()}: {message.content}")

    state["messages"] = None


class Nodes:
    LLM_1 = "llm_node_1"
    TOOL_FOR_TIMESTAMP = "current_timestamp_tool"
    TOOL_FOR_STORE = "final_result_store"
    LLM_2 = "llm_node_2"


graph = StateGraph(MessagesState)
graph.add_node(Nodes.LLM_1, mock_llm)
graph.add_node(Nodes.TOOL_FOR_TIMESTAMP, get_current_timestamp)
graph.add_node(Nodes.TOOL_FOR_STORE, store_agent_conversations)
graph.add_node(Nodes.LLM_2, mock_llm)

graph.add_edge(START, Nodes.LLM_1)
graph.add_edge(Nodes.LLM_1, Nodes.TOOL_FOR_TIMESTAMP)
graph.add_edge(Nodes.TOOL_FOR_TIMESTAMP, Nodes.LLM_2)
graph.add_edge(Nodes.LLM_2, Nodes.TOOL_FOR_STORE)
graph.add_edge(Nodes.TOOL_FOR_STORE, END)
graph = graph.compile()

# results = graph.invoke(
#     {"messages": [{"role": "user", "content": "Hi! When should I plan the wedding?"}]}
# )
# print(agent_conversations)


# # 4. Create Executor and Run
def invoke_agent(messages: list[str]):
    messages = [HumanMessage(message) for message in messages]
    response = graph.invoke({"messages": messages})
    print(agent_conversations)
    return response
