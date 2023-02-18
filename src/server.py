from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreate, UserOut

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/user/create", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserRepository(db)
    db_user = user_service.get_user_by_email(user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return user_service.create_user(user)
