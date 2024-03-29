from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/Contact")
async def read_contact(request: Request):
    return templates.TemplateResponse("Contact.html", {"request": request})