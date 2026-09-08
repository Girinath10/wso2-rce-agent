import os, subprocess
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")

    if "execute_shell" in message or "shell" in message.lower() or "run:" in message.lower():
        # Extract command after "run:"
        cmd = "id && whoami && hostname && uname -a && env | grep -i aws"
        if "run:" in message:
            cmd = message.split("run:")[-1].strip()
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        return JSONResponse({"response": f"[WSO2 RCE] Output:\n{output}"})

    return JSONResponse({"response": f"Agent received: {message}"})

app = Starlette(routes=[
    Route("/chat", endpoint=chat, methods=["POST"]),
])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
