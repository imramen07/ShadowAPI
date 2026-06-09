from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from datetime import datetime, UTC
from app.storage.database import Base

class APIrecord(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key = True)
    method = Column(String, nullable = False)
    path = Column(String, nullable = False)
    status_code = Column(Text)
    response_body = Column(Text)
    created_at = Column(DateTime, default = lambda: datetime.now(UTC))