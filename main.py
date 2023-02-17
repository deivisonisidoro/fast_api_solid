from fastapi import FastAPI

from .src.models.database import Base, engine

app = FastAPI()

# Inicialize os modelos
Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}
