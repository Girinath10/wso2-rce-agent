import os
import json
import httpx
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

MCP_URL = os.environ.get("MCP_URL", "https://onto-crm-ban-robust.trycloudflare.com")

async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")

    if "execute_shell" in message or "shell" in message.lower() or "id" in message.lower():
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                MCP_URL,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "execute_shell",
                        "arguments": {"command": "id && whoami && hostname"}
                    }
                },
                headers={"Content-Type": "application/json"}
            )
            result = resp.json()
            return JSONResponse({"response": f"Tool result: {result}"})

    return JSONResponse({"response": f"Agent received: {message}"})

app = Starlette(routes=[
    Route("/chat", endpoint=chat, methods=["POST"]),
])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
