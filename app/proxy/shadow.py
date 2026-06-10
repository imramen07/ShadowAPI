from fastapi import Response
from app.storage.crud import get_fresh_record
from app.core.logger import logger

def get_shadow_response(
        db,
        tenant_id,
        method,
        path
):
    record = get_fresh_record(
        db,
        tenant_id,
        method,
        path
    )

    if not record:
        logger.warning(f"Cache Miss: {tenant_id} - {method} {path}")
        return None
    
    #Returns Response object instead of json
    return Response(
        content = record.response_body.encode("utf-8"),
        status_code = record.status_code,
        content_type = record.content_type or "application/json"
    )