"""
Jassas Web Routes - HTML pages served via Jinja2.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

# Setup templates
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - search interface."""
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html"
    )
