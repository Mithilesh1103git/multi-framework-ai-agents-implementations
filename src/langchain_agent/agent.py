import builtins
import datetime
import os
from collections.abc import AsyncIterator, Callable, Iterator, Sequence
from typing import Any, List, Optional

import httpx
import uvicorn
from fastapi import Body, FastAPI, Request
from langchain_community.chat_models import ChatLlamaCpp
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.callbacks import CallbackManager, CallbackManagerForLLMRun
from langchain_core.language_models.base import BaseModel, LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    convert_to_messages,
)
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import BaseTool, tool
from langchain_core.utils.function_calling import convert_to_openai_tool

from langchain.agents import create_agent
from langchain.tools import tool


class GemmaLLM(BaseChatModel):

    @property
    def _llm_type(self) -> str:
        return "Google Gemma 2b LLM"

    def bind_tools(
        self,
        tools: Sequence[builtins.dict[str, Any] | type | Callable | BaseTool],
        *,
        tool_choice: str | None = None,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, AIMessage]:
        # Convert tools to JSON schema and bind to the model
        formatted_tools = [convert_to_openai_tool(tool) for tool in tools]
        return self.bind(tools=formatted_tools, **kwargs)

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:

        server_url = "http://localhost:9090/v1/chat/completions"

        tools = kwargs.get("tools")
        if tools:
            for message in messages:
                if message.type == "system":
                    message = SystemMessage(
                        message.content
                        + f" You can these tools for task execution: {tools}"
                    )

        formatted_messages = []
        for message in messages:
            if message.type == "system":
                formatted_messages.append(
                    {"role": "system", "content": message.content}
                )
            elif message.type == "human":
                formatted_messages.append({"role": "user", "content": message.content})

        data = {
            "model": "google/gemma-2b",
            "messages": formatted_messages,
            "max_tokens": 50,  # 1. LIMIT tokens so it doesn't run forever
            "temperature": 0.5,
            "stop": ["<|im_end|>", "<end_of_turn>", "user\n", "assistant\n"],
        }

        response = httpx.post(server_url, json=data, timeout=30)

        chat_result = response.json()["choices"][0]["message"]["content"]

        generated_result = ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=chat_result))]
        )

        return generated_result


@tool
def get_current_timestamp():
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


# 2. Define the LLM and Tools
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm = GemmaLLM()
tools = [get_current_timestamp]

# 3. Pull prompt and construct the agent
system_prompt = "You are an assistant model. Give the answer to user's query."
agent = create_agent(model=llm, tools=tools, system_prompt=SystemMessage(system_prompt))


# # 4. Create Executor and Run
def invoke_agent(messages: list[str]):
    messages = [HumanMessage(message) for message in messages]
    response = agent.invoke({"messages": messages})

    return response
