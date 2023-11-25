from pydantic import BaseModel


class SegmentModel(BaseModel):
    id: int
    name: str
    distance: float
    start_latlng: list[float]
    end_latlng: list[float]
    city: str | None = None
    pr_time: int | None = None
