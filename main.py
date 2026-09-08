import os
import json
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")
    session_id = body.get("session_id", "")
    return JSONResponse({
        "response": f"Agent received: {message}"
    })

app = Starlette(routes=[
    Route("/chat", endpoint=chat, methods=["POST"]),
])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
