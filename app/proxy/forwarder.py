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
    
    #Strip host header to avoid TLS verif at upstream
    if headers and "host" in headers:
        headers = {k: v for k, v in headers.items() if k.lower() != "host"}

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method = method,
            url = url,
            headers = headers,
            params = params,
            content = content
        )
    
    return response