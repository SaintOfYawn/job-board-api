from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_roles
from app.crud.company import get_by_owner
from app.crud.vacancy import create_vacancy, delete_vacancy, get_by_id, list_vacancies, update_vacancy
from app.models.user import User, UserRole
from app.models.vacancy import EmploymentType
from app.schemas.common import Page
from app.schemas.vacancy import VacancyCreate, VacancyOut, VacancyUpdate

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("", response_model=Page)
async def vacancies_list(
    db: AsyncSession = Depends(get_db),
    q: str | None = None,
    city: str | None = None,
    employment_type: EmploymentType | None = None,
    company_id: int | None = None,
    min_salary: int | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    items, total = await list_vacancies(db, q, city, employment_type, company_id, min_salary, limit, offset)
    return {"items": [VacancyOut.model_validate(x) for x in items], "total": total, "limit": limit, "offset": offset}


@router.post("", response_model=VacancyOut)
async def vacancies_create(
    payload: VacancyCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(UserRole.company, UserRole.admin)),
):
    if user.role == UserRole.admin:
        raise HTTPException(status_code=400, detail="Admin create disabled here. Use a company account.")

    company = await get_by_owner(db, user.id)
    if not company:
        raise HTTPException(status_code=400, detail="Create your company first: POST /companies/me")

    v = await create_vacancy(db, company_id=company.id, data=payload.model_dump())
    return VacancyOut.model_validate(v)


@router.patch("/{vacancy_id}", response_model=VacancyOut)
async def vacancies_update(
    vacancy_id: int,
    payload: VacancyUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    v = await get_by_id(db, vacancy_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    if user.role != UserRole.admin:
        company = await get_by_owner(db, user.id)
        if not company or v.company_id != company.id:
            raise HTTPException(status_code=403, detail="Forbidden")

    updated = await update_vacancy(db, v, payload.model_dump(exclude_unset=True))
    return VacancyOut.model_validate(updated)


@router.delete("/{vacancy_id}")
async def vacancies_delete(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    v = await get_by_id(db, vacancy_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    if user.role != UserRole.admin:
        company = await get_by_owner(db, user.id)
        if not company or v.company_id != company.id:
            raise HTTPException(status_code=403, detail="Forbidden")

    await delete_vacancy(db, v)
    return {"status": "deleted"}
