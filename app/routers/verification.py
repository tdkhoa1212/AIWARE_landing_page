from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.get("/verify")
async def verify_email(request: Request, email: str):
    verification_successful = True 

    return templates.TemplateResponse("index.html", {
        "request": request,
        "email": email,
        "verified": verification_successful  # This boolean will be used in your template.
    })



