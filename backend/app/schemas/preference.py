from pydantic import BaseModel, field_validator


class PreferenceUpdate(BaseModel):
    default_strategy: str = "auto"
    max_title_length: int = 80
    category: str | None = None

    @field_validator("max_title_length")
    @classmethod
    def length_range(cls, v: int) -> int:
        if v < 20 or v > 200:
            raise ValueError("标题长度范围应在20-200之间")
        return v


class PreferenceResponse(BaseModel):
    user_id: str
    preferences: dict

    class Config:
        from_attributes = True
