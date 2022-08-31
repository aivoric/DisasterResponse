from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .ml import router as router_ml
from .index import router as router_index
from mangum import Mangum
import os

def create_app():
    app = FastAPI()    
    static_files = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
    app.mount("/static", StaticFiles(directory=static_files), name="static")
    app.include_router(router_index.router)
    app.include_router(router_ml.router)
    return app

handler = Mangum(create_app(), lifespan="off")