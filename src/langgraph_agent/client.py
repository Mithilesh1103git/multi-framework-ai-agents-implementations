import json

import httpx

# change the following url as per deployments
server_url = "http://localhost:8080/api/v1/agent/chat/generation"


# generic http client for user query execution
def generic_http_client(url: str, messages: list[str]):
    body = {"messages": messages}

    request_response = httpx.post(url=server_url, json=body, timeout=300)

    print(f"Request status code: {request_response.status_code}")

    # request_response
    response_messages = json.loads(request_response.content.decode("utf-8"))
    print(response_messages)


# generic a2a client for agent2agent communication protocol
def generic_a2a_client(url: str, messages: list[str]):
    body = {"messages": messages}

    request_response = httpx.post(url=server_url, json=body, timeout=300)

    print(f"Request status code: {request_response.status_code}")

    # request_response
    response_messages = json.loads(request_response.content.decode("utf-8"))
    print(response_messages)


messages = ["Hi! please tell me when should I email the client?"]
response_messages = generic_http_client(url=server_url, messages=messages)
