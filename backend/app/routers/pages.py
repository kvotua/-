from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse

from app.services.exceptions import ProjectNotFoundError
from app.services.HTMLService import IHTMLService
from app.services.ProjectService.schemas.ProjectId import ProjectId

from .dependencies import get_html_service
from .exceptions import HTTPExceptionSchema

router = APIRouter(prefix="/pages", tags=["Pages"])


@router.get(
    "/{project_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def get_index_page(
    html_service: Annotated[IHTMLService, Depends(get_html_service)],
    request: Request,
    project_id: ProjectId,
) -> HTMLResponse:
    try:
        return HTMLResponse(
            content=await html_service.render_index_page(
                request=request, project_id=project_id
            )
        )
    except ProjectNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Project with this id does not exist"
        )
