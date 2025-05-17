from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from src.database import engine
from src import models
from src.routes.url import url_route
from src.routes.admin import admin_route
from src.env import NAME, HOST, CONTACT, CFTS_SITE_KEY, CFTS_SECRET_KEY

import os


# server's settings
DEFAULT_CONTEXT = { "name": NAME, "host": HOST, "contact": CONTACT }

# server's rule page
rule_f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rule.html"))
RULE = "\n".join(rule_f.readlines())


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

origins = [
    "http://127.0.0.1:8000",
    HOST
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=DEFAULT_CONTEXT | { "cfts_site_key": CFTS_SITE_KEY, "cfts_secret_key": CFTS_SECRET_KEY }
    )


@app.get("/rule", response_class=HTMLResponse)
def rule(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="rule_frame.html",
        context=DEFAULT_CONTEXT | { "rule": RULE }
    )


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context=DEFAULT_CONTEXT
    )


@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin-dashboard.html"
    )


app.include_router(admin_route.routes)

app.include_router(url_route.routes)
