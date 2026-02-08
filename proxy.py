import httpx

CORE_BACKEND_URL = "http://vm-backend:8000"

async def forward_checkin(ticket_id: str, payload: dict, headers: dict):
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.post(
            f"{CORE_BACKEND_URL}/v1/tickets/check-in/{ticket_id}",
            json=payload,
            headers=headers,
        )

    return response
