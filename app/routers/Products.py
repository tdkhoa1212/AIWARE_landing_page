from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/Products")
async def read_products(request: Request):
    return templates.TemplateResponse("Products.html", {"request": request})
