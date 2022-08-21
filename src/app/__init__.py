from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import index, ml
from mangum import Mangum
import os

def create_app():
    app = FastAPI()    
    static_files = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
    app.mount("/static", StaticFiles(directory=static_files), name="static")
    app.include_router(index.router)
    app.include_router(ml.router)
    return app

handler = Mangum(create_app(), lifespan="off")