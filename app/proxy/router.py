from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import httpx
from app.proxy.forwarder import forwardrequest
from app.storage.database import get_db
from app.storage.crud import saverecord
from app.proxy.shadow import get_shadow_response
from app.core.logger import logger
from app.proxy.auth import get_this_tenant
from app.storage.models import Tenant

router = APIRouter()

@router.api_route(
    "/{path:path}",
    methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
)
async def proxy(
    path: str,
    request: Request,
    tenant: Tenant = Depends(get_this_tenant),
    db: Session = Depends(get_db)
):
    fpath = f"/{path}" if path else "/"
    try:
        #extract params, headers, body
        params = dict(request.query_params)
        headers = dict(request.headers)
        body = await request.body()

        response = await forwardrequest(
            method = request.method,
            path = fpath,
            upstream_url = tenant.upstream_url,
            headers = headers,
            params = params,
            content = body
        )
        logger.info(f"Live Mode: {tenant.id} - {request.method} {fpath}")
        saverecord(
            db =  db,
            tenant_id = tenant.id,
            method = request.method,
            path = fpath,
            status_code = response.status_code,
            response_body = response.text,
            content_type = response.headers.get("content-type")
        )

        return Response(
            content = response.content,
            status_code = response.status_code,
            media_type = response.headers.get("content-type")
        )
    
    except (httpx.HTTPError, Exception) as e:
        logger.error(f"Upstream Error/Timeout: {tenant.id} {str(e)}. Switching to Shadow Mode.")
        logger.info(f"Shadow Mode: {tenant.id} - {request.method} /{fpath}")
        shadow_resp = get_shadow_response(
            db = db,
            tenant_id = tenant.id,
            method = request.method,
            path = fpath
        )
        if shadow_resp:
            return shadow_resp
        return JSONResponse(
            status_code = 503,
            content = {
                "error": "Upstream unavailable, cache response failed"
            }
        )