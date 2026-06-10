from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Date
from sqlalchemy import func
from datetime import datetime
from datetime import UTC
from datetime import date
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from app.storage.database import Base

class APIrecord(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key = True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable = False)
    method = Column(String, nullable = False)
    path = Column(String, nullable = False)
    status_code = Column(Integer)
    response_body = Column(Text)
    content_type = Column(String, nullable = True)
    created_at = Column(DateTime, default = lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(String, primary_key = True)
    name = Column(String, nullable = False)
    api_key_hash = Column(String, nullable = False, unique = True)
    upstream_url = Column(String, nullable = False)
    cache_ttl = Column(Integer, default = 3600)
    rate_limit_rps = Column(Integer, default = 100)
    is_active = Column(Boolean, default = True)
    created_at = Column(DateTime, default = func.now())

class Usage(Base):
    __tablename__ = "usage"
    id = Column(Integer, primary_key = True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable = False)
    date = Column(Date, default = lambda: date.today())
    requests = Column(Integer, default = 0)
    cache_hits = Column(Integer, default = 0)
    bytes_transferred = Column(Integer, default = 0)