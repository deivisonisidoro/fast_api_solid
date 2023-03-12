from fastapi import APIRouter

from src.routers import auth_routers as auth
from src.routers import user_routers as user

router = APIRouter()


router.include_router(user.router, prefix="/users", tags=["User"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
