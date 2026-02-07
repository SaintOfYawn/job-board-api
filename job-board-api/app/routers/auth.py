from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import verify_password, create_access_token
from app.crud.user import get_by_email, create_user
from app.models.user import UserRole
from app.schemas.auth import RegisterIn, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_db)):
    if await get_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, payload.email, payload.password, role=UserRole.user)
    token = create_access_token(subject=user.email, role=user.role.value)
    return TokenOut(access_token=token)


@router.post("/register-company", response_model=TokenOut)
async def register_company(payload: RegisterIn, db: AsyncSession = Depends(get_db)):
    if await get_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, payload.email, payload.password, role=UserRole.company)
    token = create_access_token(subject=user.email, role=user.role.value)
    return TokenOut(access_token=token)


@router.post("/login", response_model=TokenOut)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_by_email(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.email, role=user.role.value)
    return TokenOut(access_token=token)
