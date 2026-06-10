from fastapi import FastAPI
from app.proxy.router import router
from app.dash.dash_router import router as dash_router

app = FastAPI()
app.include_router(dash_router)
app.include_router(router)