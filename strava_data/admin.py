from django.contrib import admin

# Register your models here.
from strava_data.models import StravaAuthorization


@admin.register(StravaAuthorization)
class StravaAuthorizationAdmin(admin.ModelAdmin):
    pass
