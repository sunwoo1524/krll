from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.database import engine
from src import models
from src.routes.url import url_route


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_route.routes)

# frontend v2
app.mount("/static", StaticFiles(directory="./frontend/static"))
@app.get("/")
def frontend():
    return FileResponse("./frontend/index.html")
