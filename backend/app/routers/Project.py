from fastapi import APIRouter, HTTPException, status
from app.entities import projects, users
from app.schemas import ProjectNew, ProjectUpdate
from app.models import Project
from app.config import user_do_not_exist
from uuid import UUID

router = APIRouter(prefix="/projects")


@router.get("/{id}/", response_model=Project)
def project_get(id: UUID):
    return projects.get_by_id(id)


@router.get("/user/{id}/", response_model=list[Project])
def project_get_user(id: int):
    if users.exist(id):
        return projects.find_projects(id)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=user_do_not_exist
        )


@router.post("/add/")
def project_add(project: ProjectNew):

    if users.exist(project.user_id):
        return projects.add(project)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=user_do_not_exist
        )


@router.put("/edit/{id}/")
def project_edit(id: UUID, project: ProjectUpdate):
    projects.edit(id, project)


@router.delete("/delete/{id}/")
def project_delete(id: UUID):
    projects.delete(id)
