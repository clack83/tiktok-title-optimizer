from datetime import datetime
from pydantic import BaseModel


class SeedTitleResponse(BaseModel):
    id: str
    category: str
    title: str
    score: int
    hook_type: str | None = None
    generated_at: datetime

    class Config:
        from_attributes = True


class SeedRefreshRequest(BaseModel):
    category: str | None = None


class SeedRefreshResponse(BaseModel):
    category: str
    generated_count: int
    status: str  # "success" or "failed"


class SeedGroupedResponse(BaseModel):
    category: str
    count: int
    seeds: list[SeedTitleResponse]
