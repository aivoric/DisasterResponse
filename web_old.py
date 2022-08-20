from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
@app.get("/index", response_class=HTMLResponse)
async def root(request: Request):
    ids = [1,2,3]    
    graphJSON = [1,2,3]
    # render web page with plotly graphs
    return templates.TemplateResponse('master.html', {"request": request, "ids":ids, "graphJSON":graphJSON})


# web page that handles user query and displays model results
@app.get('/go', response_class=HTMLResponse)
async def go(request: Request):
    # save user input in query
    # query = request.args.get('query', '') 

    # use model to predict classification for query
    # classification_labels = model.predict([query])[0]
    # classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return templates.TemplateResponse(
        'go.html',
        {"request": request, "data":[1,2,3]}
        #query=query,
        #classification_result=classification_results
    )