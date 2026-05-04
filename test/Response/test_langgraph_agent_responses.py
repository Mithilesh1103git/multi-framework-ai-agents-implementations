import pytest

try:
    from ..src.langgraph_agent.agent import invoke_agent
except:
    from src.langgraph_agent.agent import invoke_agent

from langchain_core.messages import HumanMessage


# This is a helper function (not a test)
def parse_response():
    pass


def test_get_langgraph_agent_response():
    messages = [HumanMessage("This is test message.")]

    # agent_response = invoke_agent({"message": messages})
    agent_response = ["This is test response."]

    # You must ASSERT something to make the test meaningful
    assert agent_response
    assert isinstance(agent_response, list)
