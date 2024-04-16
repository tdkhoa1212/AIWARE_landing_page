from fastapi import FastAPI, Request, Depends, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from .routers import User, Auth, Verification, Products, Contact, About, Signals
import uvicorn
# from app.models.Contact import Base # If required here
# from app.Database import engine


app = FastAPI()

# Create the database tables if they don't exist
# Base.metadata.create_all(bind=engine) 

# ----------- Mounting the static files directory -----------
app.mount("/static", StaticFiles(directory="static"), name="static")


# ----------- Load pages in templates -----------
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("Index.html", {"request": request})

@app.get("/{template_name}", response_class=HTMLResponse)
async def read_template(request: Request, template_name: str):
    template_path = f"templates/{template_name}.html"  # Adjusted template path
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found")
    return templates.TemplateResponse(template_name + ".html", {"request": request})

# ----------- Including router -----------
app.include_router(User.router)
# app.include_router(Auth.router)
app.include_router(Verification.router, prefix="/verification") 
app.include_router(Products.router)
app.include_router(Contact.router)
app.include_router(About.router)
app.include_router(Signals.router)

@app.get("/favicon.ico") # Ignore requests for favicon
async def get_favicon():
    raise HTTPException(status_code=404)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
