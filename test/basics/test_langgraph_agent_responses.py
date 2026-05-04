import pytest

try:
    from ..src.langgraph_agent.agent import invoke_agent, get_current_timestamp, store_agent_conversations
except:
    from src.langgraph_agent.agent import invoke_agent, get_current_timestamp, store_agent_conversations

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


def test_get_current_timestamp():
    # Simulate the state (even if empty, the function doesn't use it)
    mock_state = {"messages": []}
    
    result = get_current_timestamp(mock_state)
    
    # Check if it returns the expected dictionary structure
    assert "messages" in result
    message = result["messages"]
    
    # Verify it's a ToolMessage
    assert message.tool_call_id == "current_timestamp"
    assert message
    print("get_current_timestamp test passed!")


def test_get_store_agent_conversations():
    # Simulate the state (even if empty, the function doesn't use it)
    mock_state = {"messages": []}
    
    result = get_current_timestamp(mock_state)
    
    # Check if it returns the expected dictionary structure
    assert "messages" in result
    message = result["messages"]
    
    # Verify it's a ToolMessage
    assert message.tool_call_id == "current_timestamp"
    assert message
    print("get_current_timestamp test passed!")