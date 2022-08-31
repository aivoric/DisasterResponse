import json
import pandas as pd
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ..templates.templates import get_templates
from ..database.database import get_database
# from .predictor import Predictor
import boto3

client = boto3.client("lambda")
templates = get_templates()
database = get_database()
df = pd.read_sql_table('disaster_messages', database)

router = APIRouter(
    prefix="/ml",
    tags=["ml"],
    responses={404: {"description": "Not found"}},
)

inputParams = {
    "Name": "Ivan"
}

@router.get("/go", response_class=HTMLResponse)
async def ml_home(request: Request, query: str):
    #predictor = Predictor(query, df)
    response = client.invoke(
        FunctionName = "",
        InvocationType = "RequestResponse",
        Payload = json.dumps(inputParams)
    )
    responseFromChild = json.load(response['Payload'])   
    # classification_result = predictor.predict()    
    data = {
        "responseFromChild": responseFromChild,
    }
    return templates.TemplateResponse("test.jinja", data)