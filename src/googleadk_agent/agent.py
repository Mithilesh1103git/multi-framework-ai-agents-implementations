from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="bartowski/google_gemma-4-E2B-it-GGUF",
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge",
)

print(dir(root_agent))

# # # 4. Create Executor and Run
# def invoke_agent(messages: list[str]):
#     messages = [HumanMessage(message) for message in messages]
#     response = agent.invoke({"messages": messages})

#     return response
