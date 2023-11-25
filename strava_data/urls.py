from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("auth/strava/", views.strava_authorize, name="strava-authorize"),
    path(
        "auth/strava/save_strava_auth/", views.save_strava_auth, name="save_strava_auth"
    ),
]
