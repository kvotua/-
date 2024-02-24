from fastapi import APIRouter

from .projects import router as projects_router
from .users import router as users_router
from .nodes import router as nodes_router

router = APIRouter()
router.include_router(router=users_router)
router.include_router(router=projects_router)
router.include_router(router=nodes_router)
