from fastapi import Response
from app.storage.crud import getrecord
from app.core.logger import logger

def get_shadow_response(
        db,
        method,
        path
):
    record = getrecord(
        db = db,
        method = method,
        path = path
    )

    if not record:
        logger.warning(f"Cache Miss: {method} {path}")
        return None
    
    #Returns Response object instead of json
    return Response(
        content = record.response_body.encode("utf-8"),
        status_code = record.status_code,
        content_type = record.content_type or "application/json"
    )