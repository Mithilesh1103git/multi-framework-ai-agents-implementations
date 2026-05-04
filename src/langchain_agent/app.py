import uvicorn
from fastapi import Body, FastAPI, Request

try:
    from agent import invoke_agent
except:
    from .agent import invoke_agent

app = FastAPI(name="Langchain AI Agent", root_path="/api/v1/agent")


# 4. Create API endpoint
@app.post("/chat/generation")
def chat_generation(messages: list[str] = Body(embed=True)):
    return invoke_agent(messages)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
