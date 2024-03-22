from fastapi import FastAPI, Request, Depends, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from .routers import user, auth, verification
import uvicorn

app = FastAPI()

# ----------- Mounting the static files directory -----------
app.mount("/static", StaticFiles(directory="static"), name="static")


# ----------- Load pages in templates -----------
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/{template_name}", response_class=HTMLResponse)
async def read_template(request: Request, template_name: str):
    template_path = f"templates/{template_name}.html"  # Adjusted template path
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found")
    return templates.TemplateResponse(template_name + ".html", {"request": request})

# ----------- Including router -----------
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(verification.router, prefix="/verification") 

@app.get("/favicon.ico") # Ignore requests for favicon
async def get_favicon():
    raise HTTPException(status_code=404)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
