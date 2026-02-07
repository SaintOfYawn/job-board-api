from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    cover_letter: str | None = None


class ApplicationOut(BaseModel):
    id: int
    user_id: int
    vacancy_id: int
    cover_letter: str | None

    model_config = {"from_attributes": True}
