from uuid import UUID

from sqlalchemy import delete, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project, Task
from app.schemas import ProjectCreate, TaskCreate


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, project_id: UUID):
        result = await self.db.execute(select(Project).where(Project.id == project_id))

        return result.scalar_one_or_none()

    async def create(self, data: ProjectCreate):
        db_obj = Project(**data.model_dump())

        self.db.add(db_obj)

        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj

    async def update(self, project_id: UUID, data: ProjectCreate):
        # TODO: just allow partial updates
        stmt = (
            update(Project)
            .where(Project.id == project_id)
            .values(**data.model_dump(exclude_unset=True))
            .returning(Project)
        )
        result = await self.db.execute(stmt)

        await self.db.commit()

        return result.scalar_one_or_none()

    async def delete(self, project_id: UUID):
        await self.db.execute(delete(Project).where(Project.id == project_id))
        await self.db.commit()


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tasks_by_priority(self, project_id: UUID, limit: int, offset: int):
        stmt = (
            select(Task)
            .where(Task.project_id == project_id)
            .order_by(desc(Task.priority))
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def create(self, project_id: UUID, data: TaskCreate):
        db_obj = Task(**data.model_dump(), project_id=project_id)

        self.db.add(db_obj)

        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj

    async def update(self, task_id: UUID, data: TaskCreate):
        stmt = (
            update(Task)
            .where(Task.id == task_id)
            .values(**data.model_dump(exclude_unset=True))
            .returning(Task)
        )

        result = await self.db.execute(stmt)

        await self.db.commit()

        return result.scalar_one_or_none()

    async def delete(self, task_id: UUID):
        await self.db.execute(delete(Task).where(Task.id == task_id))
        await self.db.commit()
