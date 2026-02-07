from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    description: str | None = None
    website: str | None = None


class CompanyOut(BaseModel):
    id: int
    name: str
    description: str | None
    website: str | None
    owner_user_id: int

    model_config = {"from_attributes": True}
