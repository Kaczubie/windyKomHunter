from django.urls import path
from . import views

urlpatterns = [
    path('auth/strava/', views.strava_authorize, name='strava_authorize'),
    path('auth/strava/callback/', views.strava_callback, name='strava_callback'),
]