from datetime import datetime
from datetime import timezone
from app.core.config import settings
from app.storage.models import APIrecord
from app.core.logger import logger

def get_fresh_record(
        db,
        tenant_id,
        method,
        path,
        max_age = None
):
    if max_age is None:
        max_age = settings.cache_ttl
    record = getrecord(db, tenant_id, method, path)
    if record and record.updated_at:
        age = (datetime.now(timezone.utc) - record.updated_at).total_seconds()
        if age > max_age:
            return None
    return record

def saverecord(
        db,
        tenant_id,
        method,
        path,
        status_code,
        response_body,
        content_type = None
):
    existing = (
        db.query(APIrecord).filter(
            APIrecord.tenant_id == tenant_id,
            APIrecord.method == method,
            APIrecord.path == path
        ).first()
    )

    if existing:
        logger.info(f"Updated: {method} {path}")
        existing.status_code = status_code
        existing.response_body = response_body
        existing.content_type = content_type
        db.commit()
        return existing
    
    logger.info(f"Recorded: {method} {path}")
    record = APIrecord(
        tenant_id = tenant_id,
        method = method,
        path = path,
        status_code = status_code,
        response_body = response_body,
        content_type = content_type
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return record

def getrecord(
        db,
        tenant_id,
        method,
        path
):
    return(
        db.query(APIrecord).filter(
            APIrecord.tenant_id == tenant_id,
            APIrecord.method == method,
            APIrecord.path == path
        ).first()
    )