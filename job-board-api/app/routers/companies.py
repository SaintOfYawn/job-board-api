from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.crud.company import create_company, get_by_owner, get_by_id
from app.models.user import User, UserRole
from app.schemas.company import CompanyCreate, CompanyOut

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/me", response_model=CompanyOut)
async def create_my_company(
    payload: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(UserRole.company, UserRole.admin)),
):
    existing = await get_by_owner(db, user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Company already exists for this user")

    c = await create_company(db, owner_user_id=user.id, name=payload.name, description=payload.description, website=payload.website)
    return CompanyOut.model_validate(c)


@router.get("/{company_id}", response_model=CompanyOut)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)):
    c = await get_by_id(db, company_id)
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")
    return CompanyOut.model_validate(c)
