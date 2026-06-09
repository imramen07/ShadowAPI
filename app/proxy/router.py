from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import httpx
from fastapi.responses import JSONResponse
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
    try:
        response = await forwardrequest(
            request.method,
            f"/{path}"
        )
        logger.info(f"Live Mode: {request.method} /{path}")
        saverecord(
            db =  db,
            method = request.method,
            path = f"/{path}",
            status_code = response.status_code,
            response_body = response.text
        )

        return response.json()
    
    except httpx.HTTPError:
        logger.info(f"Shadow Mode: {request.method} /{path}")
        shadow = get_shadow_response(
            db = db,
            method = request.method,
            path = f"/{path}"
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