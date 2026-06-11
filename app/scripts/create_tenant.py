import uuid
import hashlib
import os
from app.storage.database import SessionLocal
from app.storage.models import Tenant

db = SessionLocal()
api_key = os.urandom(24).hex()
api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

tenant = Tenant(
    id = str(uuid.uuid4()),
    name = "Test Customer",
    api_key_hash = api_key_hash,
    upstream_url = "http://httpbin.org",
    cache_ttl = 300
)
db.add(tenant)
db.commit()
print(f"Tenant ID: {tenant.id}")
print(f"API key: {api_key}")