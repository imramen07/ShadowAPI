from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.proxy.router import router
from app.dash.dash_router import router as dash_router
from app.storage.database import engine
from app.storage.models import Base

#lifespan instead of on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    Base.metadata.create_all(bind = engine)
    print("DB tables created")
    yield
    print("Shutting down")

app = FastAPI(lifespan = lifespan)

app.include_router(dash_router)
app.include_router(router)