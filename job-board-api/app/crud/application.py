from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.application import Application


async def create_application(db: AsyncSession, user_id: int, vacancy_id: int, cover_letter: str | None) -> Application:
    a = Application(user_id=user_id, vacancy_id=vacancy_id, cover_letter=cover_letter)
    db.add(a)
    await db.commit()
    await db.refresh(a)
    return a


async def list_my_applications(db: AsyncSession, user_id: int) -> list[Application]:
    return (await db.scalars(select(Application).where(Application.user_id == user_id).order_by(Application.id.desc()))).all()


async def list_vacancy_applications(db: AsyncSession, vacancy_id: int) -> list[Application]:
    return (await db.scalars(select(Application).where(Application.vacancy_id == vacancy_id).order_by(Application.id.desc()))).all()


async def get_by_id(db: AsyncSession, application_id: int) -> Application | None:
    return await db.scalar(select(Application).where(Application.id == application_id))


async def delete_application(db: AsyncSession, app: Application) -> None:
    await db.delete(app)
    await db.commit()
