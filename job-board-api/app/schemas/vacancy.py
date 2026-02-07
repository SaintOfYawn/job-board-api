from pydantic import BaseModel
from app.models.vacancy import EmploymentType


class VacancyCreate(BaseModel):
    title: str
    description: str
    city: str | None = None
    min_salary: int | None = None
    max_salary: int | None = None
    employment_type: EmploymentType = EmploymentType.full_time


class VacancyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    city: str | None = None
    min_salary: int | None = None
    max_salary: int | None = None
    employment_type: EmploymentType | None = None


class VacancyOut(BaseModel):
    id: int
    title: str
    description: str
    city: str | None
    min_salary: int | None
    max_salary: int | None
    employment_type: EmploymentType
    company_id: int

    model_config = {"from_attributes": True}
