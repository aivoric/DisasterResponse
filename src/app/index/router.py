"""
Homepage of the web app.
"""
import json
import pandas as pd
import numpy as np
import plotly
from plotly.graph_objs import Bar
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ..templates.templates import get_templates
from ..database.database import get_database

templates = get_templates()
database = get_database()
df = pd.read_sql_table('disaster_messages', database)

router = APIRouter(
    prefix="",
    tags=["home"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Handle the request for the homepage.

    Group the data from SQLLite DB via pandas, render index.jinja template with the relevant data.
    """
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        }
    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    data = {
        "request": request,
        "ids": ids,
        "graphJSON": graphJSON
    }

    return templates.TemplateResponse("index.jinja", data)