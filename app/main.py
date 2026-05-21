from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import randomization, steps

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Forró Passos Condutor")
app.include_router(steps.router)
app.include_router(randomization.router)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def index():
    return templates.get_template("index.html").render()
