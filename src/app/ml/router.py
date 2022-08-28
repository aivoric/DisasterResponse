import pandas as pd
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ..templates.templates import get_templates
from ..database.database import get_database
from .predictor import Predictor

templates = get_templates()
database = get_database()
df = pd.read_sql_table('disaster_messages', database)

router = APIRouter(
    prefix="/ml",
    tags=["ml"],
    responses={404: {"description": "Not found"}},
)

@router.get("/go", response_class=HTMLResponse)
async def ml_home(request: Request, query: str):
    predictor = Predictor(query, df)
    classification_result = predictor.predict()    
    data = {
        "request": request,
        "query": query,
        "classification_result": classification_result
    }
    return templates.TemplateResponse("go.jinja", data)