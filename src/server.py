import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src.config.settings import Settings
from src.routers.router import router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI(title="English Course API", version="0.0.1", docs_url="/swagger/doc", redoc_url="/swagger/redoc")
settings = Settings()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Doc Redirect"])
def redirect():
    return RedirectResponse(url="/swagger/doc")


app.include_router(router, prefix="/api")
