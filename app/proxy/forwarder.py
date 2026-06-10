import httpx

TARGET_URL = "https://brokenapi123456.com"

async def forwardrequest(
        method: str,
        path: str,
        headers: dict = None,
        params: dict = None,
        content: bytes = None
):
    url = f"{TARGET_URL}{path}"

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method = method,
            url = url,
            headers = headers,
            params = params,
            content = content,
            timeout = 10.0
        )
    
    return response