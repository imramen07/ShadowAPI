import httpx
from app.core.config import settings

async def forwardrequest(
        method: str,
        path: str,
        upstream_url: str,
        headers: dict = None,
        params: dict = None,
        content: bytes = None
):
    url = f"{upstream_url}{path}"

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method = method,
            url = url,
            headers = headers,
            params = params,
            content = content,
            timeout = settings.req_timeout
        )
    
    return response