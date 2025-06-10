from fastapi import APIRouter, Request

from src.main import templates

router = APIRouter(
    prefix="/",
    tags=["Index page"],
)

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        name="user/index.html",
        request=request,
        content={},
    )