from fastapi import Request
from fastapi.responses import JSONResponse

def check_agent(request: Request):
    user_agent = request.headers.get("user-agent", "").lower()

    if "raspberry" not in user_agent and "python-httpx" not in user_agent:
        return JSONResponse(
            status_code=403,
            content={"detail": "Forbidden client"},
        )

    return None
