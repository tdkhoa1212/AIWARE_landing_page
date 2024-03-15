from fastapi import FastAPI, Request, Depends, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from .routers import user 
import uvicorn

app = FastAPI()

# Mounting the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_template_items(): # Dependency to get the list of items in the templates folder
    templates_dir = "templates"
    template_files = os.listdir(templates_dir)
    return [file[:-5] for file in template_files if file.endswith(".html")]

@app.get("/", response_class=HTMLResponse) # Route to serve the index.html file
async def read_root(request: Request, templates_list: list = Depends(get_template_items)):
    return templates.TemplateResponse("index.html", {"request": request, "templates_list": templates_list})

@app.get("/{template_name}", response_class=HTMLResponse) # Route to serve individual template pages
async def read_template(request: Request, template_name: str):
    template_path = f"{template_name}.html"
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found")
    return templates.TemplateResponse(template_path, {"request": request, "template_name": template_name})

app.include_router(user.router)

@app.get("/favicon.ico") # Ignore requests for favicon
async def get_favicon():
    raise HTTPException(status_code=404)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
