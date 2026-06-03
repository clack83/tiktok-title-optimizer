from pydantic import BaseModel, field_validator


class OptimizeRequest(BaseModel):
    title: str
    strategy: str = "auto"
    category: str | None = None
    count: int = 4

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("标题不能为空")
        if len(v) > 200:
            raise ValueError("标题长度不能超过200字")
        return v.strip()

    @field_validator("count")
    @classmethod
    def count_range(cls, v: int) -> int:
        if v < 1 or v > 10:
            raise ValueError("生成数量应在1-10之间")
        return v


class ScoreRequest(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("标题不能为空")
        if len(v) > 200:
            raise ValueError("标题长度不能超过200字")
        return v.strip()


class KeywordsRequest(BaseModel):
    title: str


class BatchOptimizeRequest(BaseModel):
    titles: list[str]
    strategy: str = "auto"
    category: str | None = None

    @field_validator("titles")
    @classmethod
    def titles_limit(cls, v: list[str]) -> list[str]:
        if len(v) == 0:
            raise ValueError("至少需要1条标题")
        if len(v) > 50:
            raise ValueError("批量优化最多支持50条标题")
        return [t.strip() for t in v if t.strip()]


class CompareRequest(BaseModel):
    record_id_1: str
    record_id_2: str


class HistoryQuery(BaseModel):
    page: int = 1
    page_size: int = 20
    start_date: str | None = None
    end_date: str | None = None
