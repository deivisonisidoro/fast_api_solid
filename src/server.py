from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src.routers import router

load_dotenv()

app = FastAPI(
    title="Anime Search API",
    version="0.0.1",
)

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
    return RedirectResponse(url="/docs/")


app.include_router(router, prefix="/api")
