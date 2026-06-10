from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import Header
from app.storage.database import get_db
from app.storage.models import APIrecord
from app.core.config import settings

def verify_admin_token(
        authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(
            status_code = 401,
            detail = "Missing Authorization"
        )
    scheme, token = authorization.split()
    if scheme.lower() != "bearer" or token != settings.admin_token:
        raise HTTPException(
            status_code = 401,
            detail = ("Invalid Token")
        )
    return True

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
    db: Session = Depends(get_db),
    _=Depends(verify_admin_token)
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
    db: Session = Depends(get_db),
    _=Depends(verify_admin_token)
):
    total_routes = db.query(APIrecord).count()

    return {
        "cached_routes": total_routes
    }