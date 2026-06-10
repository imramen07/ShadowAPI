import hashlib
from fastapi import Header
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from app.storage.database import get_db
from app.storage.models import Tenant

async def get_this_tenant(
        x_api_key: str = Header(..., alias = "X-API-Key"),
        db: Session = Depends(get_db)
) -> Tenant:
    if not x_api_key:
        raise HTTPException(401, "Missing X-API-Key Header")
    
    key_hash = hashlib.sha256(x_api_key.encode()).hexdigest()
    tenant = db.query(Tenant).filter(
        Tenant.api_key_hash == key_hash,
        Tenant.is_active == True
    ).first()
    if not tenant:
        raise HTTPException(401, "Invalid or Inactive API key")
    return tenant