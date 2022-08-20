from fastapi import APIRouter, Request
from ..helpers.templates import get_templates
from fastapi.responses import HTMLResponse

templates = get_templates()

router = APIRouter(
    prefix="/ml",
    tags=["ml"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_class=HTMLResponse)
async def ml_home(request: Request):
    return templates.TemplateResponse("master.html", {"request": request})