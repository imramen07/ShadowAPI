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

router = APIRouter()

@router.api_route(
    "/{path:path}",
    methods = ["GET"]
)
async def proxy(
    path: str,
    request: Request,
    db: Session = Depends(get_db)
):
    fpath = f"/{path}"
    try:
        #extract params, headers, body
        params = dict(request.query_params)
        headers = dict(request.headers)
        body = await request.body()

        response = await forwardrequest(
            method = request.method,
            path = fpath,
            headers = headers,
            params = params,
            content = body
        )
        logger.info(f"Live Mode: {request.method} /{path}")
        saverecord(
            db =  db,
            method = request.method,
            path = fpath,
            status_code = response.status_code,
            response_body = response.text
        )

        return Response(
            content = response.content,
            status_code = response.status_code,
            media = response.headers.get("content-type")
        )
    
    except (httpx.HTTPError, Exception) as e:
        logger.error(f"Upstream Error/Timeout: {str(e)}. Switching to Shadow Mode.")
        logger.info(f"Shadow Mode: {request.method} /{fpath}")
        shadow = get_shadow_response(
            db = db,
            method = request.method,
            path = fpath
        )
        if shadow:
            return JSONResponse(
                content = shadow["body"],
                status_code = shadow["status_code"]
            )
        return JSONResponse(
            status_code = 503,
            content = {
                "error": "Upstream unavailable, cache response failed"
            }
        )