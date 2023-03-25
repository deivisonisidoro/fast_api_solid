"""
A module that defines an APIRouter instance and registers various routes.

This module imports two modules: auth_routers and user_routers from the src.routers package.
These modules define the authentication and user routes respectively.

Attributes:
    router (APIRouter): An instance of the APIRouter class provided by FastAPI.

Examples:
    To include the user routes, you can call the `include_router` method on the router instance:
    
    >>> from src.api import router
    >>> from src.routers.user_routers import router as user_router
    >>> router.include_router(user_router, prefix="/users", tags=["User"])

    To include the authentication routes, you can call the `include_router` method on the router instance:
    
    >>> from src.api import router
    >>> from src.routers.auth_routers import router as auth_router
    >>> router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
"""
from fastapi import APIRouter

from src.routers import auth_routers as auth
from src.routers import user_routers as user

router = APIRouter()


router.include_router(user.router, prefix="/users", tags=["User"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
