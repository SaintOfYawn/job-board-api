from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.company import Company


async def get_by_id(db: AsyncSession, company_id: int) -> Company | None:
    return await db.scalar(select(Company).where(Company.id == company_id))


async def get_by_owner(db: AsyncSession, owner_user_id: int) -> Company | None:
    return await db.scalar(select(Company).where(Company.owner_user_id == owner_user_id))


async def create_company(db: AsyncSession, owner_user_id: int, name: str, description: str | None, website: str | None) -> Company:
    c = Company(owner_user_id=owner_user_id, name=name, description=description, website=website)
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return c
