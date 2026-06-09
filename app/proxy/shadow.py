import json
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
    
    return {
        "status_code": record.status_code,
        "body": json.loads(record.response_body)
    }