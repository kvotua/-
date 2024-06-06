from fastapi import APIRouter

from .attributes import router as attribute_router
from .nodes import router as nodes_router
from .projects import router as projects_router
from .templates import router as templates_router
from .users import router as users_router

router = APIRouter()
router.include_router(router=users_router)
router.include_router(router=projects_router)
router.include_router(router=nodes_router)
router.include_router(router=templates_router)
router.include_router(router=attribute_router)
