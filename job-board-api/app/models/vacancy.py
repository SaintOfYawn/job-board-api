import enum
from sqlalchemy import String, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class EmploymentType(str, enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    internship = "internship"


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(String(6000))
    city: Mapped[str | None] = mapped_column(String(120), default=None)

    min_salary: Mapped[int | None] = mapped_column(Integer, default=None)
    max_salary: Mapped[int | None] = mapped_column(Integer, default=None)

    employment_type: Mapped[EmploymentType] = mapped_column(Enum(EmploymentType, name="employment_type"), default=EmploymentType.full_time)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), index=True)
    company = relationship("Company")
