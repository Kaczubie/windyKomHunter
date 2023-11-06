from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings

def strava_authorize(request):
    strava_url = f'https://www.strava.com/oauth/authorize?client_id={settings.STRAVA_CLIENT_ID}&redirect_uri={settings.STRAVA_REDIRECT_URI}&response_type=code&scope=read,activity:read_all'
    return redirect(strava_url)

def strava_callback(request):
    code = request.GET.get('code')
    token_url = 'https://www.strava.com/oauth/token'

    data = {
        'client_id': settings.STRAVA_CLIENT_ID,
        'client_secret': settings.STRAVA_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, data=data)
    strava_data = response.json()

    # You can now use strava_data to access the user's Strava information and access tokens.
    # For example, you can save the access token to authenticate future Strava API requests.

    return HttpResponse('Strava authorization successful!')