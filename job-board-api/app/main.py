from fastapi import FastAPI
from app.core.config import settings
from app.routers.auth import router as auth_router
from app.routers.companies import router as companies_router
from app.routers.vacancies import router as vacancies_router
from app.routers.applications import router as applications_router

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth_router)
app.include_router(companies_router)
app.include_router(vacancies_router)
app.include_router(applications_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
