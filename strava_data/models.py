import json
from typing import Any

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils import timezone

from .schemas import StravaTokenResponse


class StravaAuthorization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=200)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    scope = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)

    def has_valid_access_token(self) -> bool:
        return (
            self.access_token and not self.is_token_expired() and self.has_valid_scope()
        )

    def is_token_expired(self) -> bool:
        return self.expires_at <= timezone.now() if self.expires_at else True

    def has_valid_scope(self):
        """Return true if the scope is valid."""
        return "activity:read" in self.scope

    def set_scope(self, value):
        self.scope = json.dumps(value)

    def get_scope(self):
        return json.loads(self.scope) if self.scope else []

    @classmethod
    def create_with_scope(cls, scope_list: list[str], **kwargs: Any):
        instance = cls(**kwargs)
        instance.set_scope(scope_list)
        instance.save()
        return instance

    def update_token(self, token_response: StravaTokenResponse):
        """Update the token with the response from strava."""
        self.access_token = token_response.access_token
        self.refresh_token = token_response.refresh_token
        self.expires_at = token_response.expires_at_datetime
        self.save()

    def __str__(self) -> str:
        return (
            f"{self.user.username.capitalize()} "
            f"{'has' if self.has_valid_access_token() else 'does not have'} "
            f"valid access token"
        )
