from django.urls import path
from . import views

urlpatterns = [
    path("auth/strava/", views.strava_authorize, name="strava_authorize"),
    path(
        "auth/strava/save_strava_auth/", views.save_strava_auth, name="save_strava_auth"
    ),
]
