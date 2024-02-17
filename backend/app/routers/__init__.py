from fastapi import APIRouter

from .projects.views import router as projects_router
from .users.views import router as users_router

router = APIRouter()
router.include_router(router=users_router)
router.include_router(router=projects_router)
