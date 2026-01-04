"""
Jassas Web Routes - HTML pages served via Jinja2.
"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import time

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


@router.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = Query("", min_length=0)):
    """Search results page."""
    if not q or len(q) < 2:
        return templates.TemplateResponse(
            request=request,
            name="pages/search.html",
            context={"query": q, "results": [], "count": 0, "execution_time_ms": 0}
        )

    # Get ranker from app state
    ranker = getattr(request.app.state, "ranker", None)
    if not ranker:
        return templates.TemplateResponse(
            request=request,
            name="pages/search.html",
            context={"query": q, "results": [], "count": 0, "execution_time_ms": 0, "error": "محرك البحث غير جاهز"}
        )

    start_time = time.perf_counter()
    raw_results = ranker.search(query=q, k=10)
    execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

    # Format results
    results = []
    for res in raw_results:
        snippet = res.get("clean_text", "")[:200]
        if len(res.get("clean_text", "")) > 200:
            snippet += "..."
        results.append({
            "title": res.get("title") or "بدون عنوان",
            "url": res.get("url") or "",
            "snippet": snippet,
            "score": round(res.get("score", 0.0), 4)
        })

    return templates.TemplateResponse(
        request=request,
        name="pages/search.html",
        context={
            "query": q,
            "results": results,
            "count": len(results),
            "execution_time_ms": execution_time_ms
        }
    )


@router.get("/search/results", response_class=HTMLResponse)
async def search_results_partial(request: Request, q: str = Query("", min_length=0)):
    """HTMX partial - returns only results HTML."""
    if not q or len(q) < 2:
        return templates.TemplateResponse(
            request=request,
            name="components/results.html",
            context={"query": q, "results": []}
        )

    ranker = getattr(request.app.state, "ranker", None)
    if not ranker:
        return templates.TemplateResponse(
            request=request,
            name="components/results.html",
            context={"query": q, "results": [], "error": "محرك البحث غير جاهز"}
        )

    raw_results = ranker.search(query=q, k=10)

    results = []
    for res in raw_results:
        snippet = res.get("clean_text", "")[:200]
        if len(res.get("clean_text", "")) > 200:
            snippet += "..."
        results.append({
            "title": res.get("title") or "بدون عنوان",
            "url": res.get("url") or "",
            "snippet": snippet,
            "score": round(res.get("score", 0.0), 4)
        })

    return templates.TemplateResponse(
        request=request,
        name="components/results.html",
        context={"query": q, "results": results}
    )
