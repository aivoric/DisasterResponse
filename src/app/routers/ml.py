import pandas as pd
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ..helpers.templates import get_templates
from ..helpers.database import get_database_engine
from ..ml.predictor import Predictor

templates = get_templates()
engine = get_database_engine()
df = pd.read_sql_table('disaster_messages', engine)

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