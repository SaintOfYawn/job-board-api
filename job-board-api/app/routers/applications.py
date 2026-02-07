from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db, require_roles
from app.crud.application import (
    create_application,
    delete_application,
    get_by_id as get_app_by_id,
    list_my_applications,
    list_vacancy_applications,
)
from app.crud.company import get_by_owner
from app.crud.vacancy import get_by_id as get_vacancy_by_id
from app.models.user import User, UserRole
from app.schemas.application import ApplicationCreate, ApplicationOut

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/vacancy/{vacancy_id}", response_model=ApplicationOut)
async def apply_to_vacancy(
    vacancy_id: int,
    payload: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(UserRole.user, UserRole.admin)),
):
    v = await get_vacancy_by_id(db, vacancy_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    try:
        a = await create_application(db, user_id=user.id, vacancy_id=vacancy_id, cover_letter=payload.cover_letter)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="You have already applied to this vacancy")

    return ApplicationOut.model_validate(a)


@router.get("/me", response_model=list[ApplicationOut])
async def my_applications(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(UserRole.user, UserRole.admin)),
):
    items = await list_my_applications(db, user.id)
    return [ApplicationOut.model_validate(x) for x in items]


@router.get("/vacancy/{vacancy_id}", response_model=list[ApplicationOut])
async def vacancy_applications(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    v = await get_vacancy_by_id(db, vacancy_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    if user.role != UserRole.admin:
        company = await get_by_owner(db, user.id)
        if not company or v.company_id != company.id:
            raise HTTPException(status_code=403, detail="Forbidden")

    items = await list_vacancy_applications(db, vacancy_id)
    return [ApplicationOut.model_validate(x) for x in items]


@router.delete("/{application_id}")
async def delete_my_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    a = await get_app_by_id(db, application_id)
    if not a:
        raise HTTPException(status_code=404, detail="Application not found")

    if user.role != UserRole.admin and a.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    await delete_application(db, a)
    return {"status": "deleted"}
