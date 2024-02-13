from fastapi import APIRouter

from app.api_v1.projects.views import router as projects_router
from app.api_v1.users.views import router as users_router
from app.core.config import settings

router = APIRouter(prefix=settings.api_v1_prefix)
router.include_router(router=users_router)
router.include_router(router=projects_router)
