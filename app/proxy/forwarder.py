import httpx

TARGET_URL = "https://brokenapi123456.com"

async def forwardrequest(
        method,
        path
):
    url = f"{TARGET_URL}{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method = method,
            url = url
        )
    
    return response