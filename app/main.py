from contextlib import asynccontextmanager
from typing import List
from uuid import UUID

from fastapi import Depends, FastAPI, Header, HTTPException

from app import schemas
from app.database import init_db
from app.deps import get_project_repo, get_task_repo
from app.services import ProjectRepository, TaskRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


API_KEY_SECRET = "some-api-key"


async def verify_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Invalid API Key")


app = FastAPI(
    title="Project Management",
    lifespan=lifespan,
    dependencies=[Depends(verify_api_key)],
)


@app.post("/projects/", response_model=schemas.Project, status_code=201)
async def create_project(
    project: schemas.ProjectCreate, repo: ProjectRepository = Depends(get_project_repo)
):
    return await repo.create(project)


@app.get("/projects/{project_id}", response_model=schemas.Project)
async def read_project(
    project_id: UUID, repo: ProjectRepository = Depends(get_project_repo)
):
    project = await repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/projects/{project_id}", response_model=schemas.Project)
async def update_project(
    project_id: UUID,
    data: schemas.ProjectCreate,
    repo: ProjectRepository = Depends(get_project_repo),
):
    project = await repo.update(project_id, data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.delete("/projects/{project_id}", status_code=204)
async def delete_project(
    project_id: UUID, repo: ProjectRepository = Depends(get_project_repo)
):
    await repo.delete(project_id)
    return None


@app.post("/projects/{project_id}/tasks/", response_model=schemas.Task)
async def create_task(
    project_id: UUID,
    task: schemas.TaskCreate,
    project_repo: ProjectRepository = Depends(get_project_repo),
    task_repo: TaskRepository = Depends(get_task_repo),
):
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return await task_repo.create(project_id, task)


@app.get("/projects/{project_id}/tasks/", response_model=List[schemas.Task])
async def list_tasks(
    project_id: UUID,
    limit: int = 10,
    offset: int = 0,
    project_repo: ProjectRepository = Depends(get_project_repo),
    task_repo: TaskRepository = Depends(get_task_repo),
):
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return await task_repo.get_tasks_by_priority(project_id, limit, offset)


@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: UUID,
    task: schemas.TaskCreate,
    repo: TaskRepository = Depends(get_task_repo),
):
    updated_task = await repo.update(task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: UUID, repo: TaskRepository = Depends(get_task_repo)):
    await repo.delete(task_id)
    return None
