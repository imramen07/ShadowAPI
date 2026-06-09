from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.storage.database import get_db
from app.storage.models import APIrecord

router = APIRouter(
    prefix = "/shadow",
    tags = ["ShadowAPI Dashboard"]
)

@router.get("/status")
def status():
    return {
        "service": "ShadowAPI",
        "status": "running"
    }

@router.get("/routes")
def routes(
    db: Session = Depends(get_db)
):
    records = db.query(APIrecord).all()

    return [
        {
            "method": r.method,
            "path": r.path,
            "status_code": r.status_code
        }
        for r in records
    ]

@router.get("/stats")
def stats(
    db: Session = Depends(get_db)
):
    total_routes = db.query(APIrecord).count()

    return {
        "cached_routes": total_routes
    }