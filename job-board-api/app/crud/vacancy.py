from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vacancy import Vacancy, EmploymentType


async def get_by_id(db: AsyncSession, vacancy_id: int) -> Vacancy | None:
    return await db.scalar(select(Vacancy).where(Vacancy.id == vacancy_id))


async def create_vacancy(db: AsyncSession, company_id: int, data: dict) -> Vacancy:
    v = Vacancy(company_id=company_id, **data)
    db.add(v)
    await db.commit()
    await db.refresh(v)
    return v


async def update_vacancy(db: AsyncSession, vacancy: Vacancy, data: dict) -> Vacancy:
    for k, v in data.items():
        setattr(vacancy, k, v)
    await db.commit()
    await db.refresh(vacancy)
    return vacancy


async def delete_vacancy(db: AsyncSession, vacancy: Vacancy) -> None:
    await db.delete(vacancy)
    await db.commit()


async def list_vacancies(
    db: AsyncSession,
    q: str | None,
    city: str | None,
    employment_type: EmploymentType | None,
    company_id: int | None,
    min_salary: int | None,
    limit: int,
    offset: int,
) -> tuple[list[Vacancy], int]:
    stmt = select(Vacancy)
    count_stmt = select(func.count(Vacancy.id))

    if q:
        stmt = stmt.where(Vacancy.title.ilike(f"%{q}%"))
        count_stmt = count_stmt.where(Vacancy.title.ilike(f"%{q}%"))
    if city:
        stmt = stmt.where(Vacancy.city == city)
        count_stmt = count_stmt.where(Vacancy.city == city)
    if employment_type:
        stmt = stmt.where(Vacancy.employment_type == employment_type)
        count_stmt = count_stmt.where(Vacancy.employment_type == employment_type)
    if company_id:
        stmt = stmt.where(Vacancy.company_id == company_id)
        count_stmt = count_stmt.where(Vacancy.company_id == company_id)
    if min_salary is not None:
        stmt = stmt.where((Vacancy.max_salary.is_(None)) | (Vacancy.max_salary >= min_salary))
        count_stmt = count_stmt.where((Vacancy.max_salary.is_(None)) | (Vacancy.max_salary >= min_salary))

    total = await db.scalar(count_stmt)
    items = (await db.scalars(stmt.order_by(Vacancy.id.desc()).limit(limit).offset(offset))).all()
    return items, int(total or 0)
