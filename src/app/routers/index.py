from fastapi import APIRouter, Request
from ..helpers.templates import get_templates
from fastapi.responses import HTMLResponse

templates = get_templates()

router = APIRouter(
    prefix="",
    tags=["home", "hello"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})