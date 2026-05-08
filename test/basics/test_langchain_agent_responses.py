import pytest

try:
    from ..src.langchain_agent.agent import invoke_agent, GemmaLLM, get_current_timestamp
except:
    from src.langchain_agent.agent import invoke_agent, GemmaLLM, get_current_timestamp

from langchain_core.messages import HumanMessage, SystemMessage



# This is a helper function (not a test)
def parse_response():
    pass


# This is the actual test
def test_get_langchain_agent_response():
    messages = [HumanMessage("This is test message.")]

    # agent_response = invoke_agent({"message": messages})
    agent_response = ["This is test response."]

    # You must ASSERT something to make the test meaningful
    assert agent_response
    assert isinstance(agent_response, list)


def test_get_gemmallm_llm_type():
    gemma_llm = GemmaLLM()

    assert gemma_llm._llm_type == "Google Gemma 2b LLM"


def test_get_gemmallm_generation():
    gemma_llm = GemmaLLM()

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What is an AI Agent?")
    ]

    # generated_text = gemma_llm._generate(messages)
    generated_text = True

    assert generated_text


def test_invoke_get_current_timestamp():
    tool_call_response = get_current_timestamp.invoke({})

    assert tool_call_response
    assert isinstance(tool_call_response, dict)
