from datetime import datetime

from django.utils import timezone
from pydantic import BaseModel, Field


class StravaAthleteData(BaseModel):
    """Class to parse strava user data."""

    strava_id: int = Field(..., alias="id")
    username: str | None = Field(default=None)
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    resource_state: int | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    sex: str | None = Field(default=None)
    premium: bool | None = Field(default=None)
    summit: bool | None = Field(default=None)
    weight: float | None = Field(default=None)
    profile_medium: str | None = Field(default=None)
    profile: str | None = Field(default=None)


class StravaTokenResponse(BaseModel):
    """Class to parse strava token responses."""

    access_token: str
    expires_at: int
    refresh_token: str
    athlete: StravaAthleteData | None = Field(default=None)

    @property
    def expires_at_datetime(self) -> datetime:
        """Get a datetime from the expires_at timestamp."""
        return timezone.make_aware(datetime.fromtimestamp(self.expires_at))
