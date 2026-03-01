import os
import sys
import re
import getpass


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "create_admin":
        # Import only what the CLI needs — avoids loading the full FastAPI app
        from src.database import engine, SessionLocal
        from src import models

        def cmd_create_admin():
            """Interactive CLI to create an admin account."""
            models.Base.metadata.create_all(bind=engine)

            print("=== Krll: Create Admin Account ===")

            while True:
                username = input("Username: ").strip()
                if not username:
                    print("Error: Username cannot be empty.")
                    continue
                if re.fullmatch(r"[A-Za-z0-9_]+", username) is None:
                    print("Error: Username may only contain letters, digits, and underscores.")
                    continue
                break

            while True:
                password = getpass.getpass("Password: ")
                if len(password) < 8:
                    print("Error: Password must be at least 8 characters.")
                    continue
                password_confirm = getpass.getpass("Confirm password: ")
                if password != password_confirm:
                    print("Error: Passwords do not match.")
                    continue
                break

            from src.routes.admin.admin_crud import get_admin, create_admin_in_db
            db = SessionLocal()
            try:
                if get_admin(db, username):
                    print(f"Error: Username '{username}' already exists.")
                    sys.exit(1)
                create_admin_in_db(db, username, password)
                print(f"Admin account '{username}' created successfully.")
            finally:
                db.close()

        cmd_create_admin()
        sys.exit(0)
    else:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
        sys.exit(0)


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from src.database import engine
from src import models
from src.routes.url import url_route
from src.routes.admin import admin_route
from src.env import NAME, HOST, CONTACT, site_key, secret_key, CAPTCHA_MODE, cap_instance


# server's settings
DEFAULT_CONTEXT = { "name": NAME, "host": HOST, "contact": CONTACT }

# server's rule page
rule_f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rule.html"))
RULE = "\n".join(rule_f.readlines())
rule_f.close()


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
        context=DEFAULT_CONTEXT | { "captcha_mode": CAPTCHA_MODE, "captcha_site_key": site_key, "captcha_secret_key": secret_key, "cap_instance": cap_instance }
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
