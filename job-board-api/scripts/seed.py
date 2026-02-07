import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.company import Company
from app.models.vacancy import Vacancy, EmploymentType
from app.models.application import Application

DEMO = {
    "company_email": "company@example.com",
    "company_password": "company123",
    "user_email": "user@example.com",
    "user_password": "user123",
}


async def get_or_create_user(db: AsyncSession, email: str, password: str, role: UserRole) -> User:
    u = await db.scalar(select(User).where(User.email == email))
    if u:
        return u
    u = User(email=email, hashed_password=hash_password(password), role=role)
    db.add(u)
    await db.commit()
    await db.refresh(u)
    return u


async def main():
    async with AsyncSessionLocal() as db:
        company_user = await get_or_create_user(db, DEMO["company_email"], DEMO["company_password"], UserRole.company)
        normal_user = await get_or_create_user(db, DEMO["user_email"], DEMO["user_password"], UserRole.user)

        company = await db.scalar(select(Company).where(Company.owner_user_id == company_user.id))
        if not company:
            company = Company(
                owner_user_id=company_user.id,
                name="Acme Corp",
                description="Demo company for Job Board API",
                website="https://example.com",
            )
            db.add(company)
            await db.commit()
            await db.refresh(company)

        existing = (await db.scalars(select(Vacancy).where(Vacancy.company_id == company.id))).all()
        if not existing:
            v1 = Vacancy(
                company_id=company.id,
                title="Junior Python Developer",
                description="FastAPI, PostgreSQL, Docker. Great for juniors.",
                city="Remote",
                min_salary=800,
                max_salary=1400,
                employment_type=EmploymentType.full_time,
            )
            v2 = Vacancy(
                company_id=company.id,
                title="Frontend React Developer",
                description="React, REST integration.",
                city="Oslo",
                min_salary=900,
                max_salary=1600,
                employment_type=EmploymentType.contract,
            )
            db.add_all([v1, v2])
            await db.commit()
            await db.refresh(v1)
            await db.refresh(v2)
        else:
            v1 = existing[0]

        app = await db.scalar(select(Application).where(Application.user_id == normal_user.id, Application.vacancy_id == v1.id))
        if not app:
            app = Application(user_id=normal_user.id, vacancy_id=v1.id, cover_letter="Hi! This is a demo application.")
            db.add(app)
            await db.commit()

    print("Seed completed ✅")
    print("Demo credentials:")
    print(f"  Company: {DEMO['company_email']} / {DEMO['company_password']}")
    print(f"  User:    {DEMO['user_email']} / {DEMO['user_password']}")


if __name__ == "__main__":
    asyncio.run(main())
