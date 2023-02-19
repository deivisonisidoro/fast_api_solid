from fastapi import APIRouter

from src.controllers import user_controller as user

router = APIRouter()


router.include_router(user.router, prefix="/users", tags=["User"])
