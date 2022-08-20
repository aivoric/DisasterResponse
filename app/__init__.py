from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import index, ml

def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.include_router(index.router)
    app.include_router(ml.router)
    return app

