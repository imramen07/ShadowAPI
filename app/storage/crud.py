from app.storage.models import APIrecord
from app.core.logger import logger

def saverecord(
        db,
        method,
        path,
        status_code,
        response_body
):
    existing = (
        db.query(APIrecord).filter(
            APIrecord.method == method,
            APIrecord.path == path
        ).first()
    )

    if existing:
        logger.info(f"Updated: {method} {path}")
        existing.status_code = status_code
        existing.response_body = response_body

        db.commit()

        return existing
    
    logger.info(f"Recorded: {method} {path}")
    record = APIrecord(
        method = method,
        path = path,
        status_code = status_code,
        response_body = response_body
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return record

def getrecord(
        db,
        method,
        path
):
    return(
        db.query(APIrecord).filter(
            APIrecord.method == method,
            APIrecord.path == path
        ).first()
    )