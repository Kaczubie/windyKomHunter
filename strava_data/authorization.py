import enum
import logging

import requests
from django.contrib.auth.models import User

from strava_data.models import StravaAuthorization
from strava_data.schemas import StravaTokenResponse
from windy_kom_hunter import settings

logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

ACCESS_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=read,activity:read_all"
STRAVA_REDIRECT_URI = "http://{http_host}/strava_data/auth/strava/save_strava_auth/"





def get_authentication(user: User):
    """Returns the strava authentication for a user if it exists and is valid.
    If token is expired, it will try to refresh it."""
    try:
        strava_auth = StravaAuthorization.objects.get(user=user)
    except StravaAuthorization.DoesNotExist:
        return None

    if strava_auth.has_valid_access_token():
        logger.debug(f"User {user} has valid token")
        return strava_auth

    if strava_auth.is_token_expired:
        logger.debug(f"User {user} has expired token. Will try to refresh.")
        refresh_token(strava_auth)
        if strava_auth.has_valid_access_token():
            logger.debug("Token refreshed")
            return strava_auth
        else:
            logger.debug("Token couldn't be refreshed")

    return None

def get_authorization_url(http_host: str) -> str:

    return STRAVA_AUTH_URL.format(
        client_id=settings.STRAVA_CLIENT_ID,
        redirect_uri=STRAVA_REDIRECT_URI.format(http_host=http_host),
    )


def request_access_token(strava_auth: StravaAuthorization):
    """Requests an access token for a user."""
    _access_token_update(strava_auth, refresh=False)

def refresh_token(strava_auth: StravaAuthorization):
    """Refreshes the access token for a user."""
    _access_token_update(strava_auth, refresh=True)

def _access_token_update(strava_auth: StravaAuthorization, refresh=False):
    """Updates the access token for a user. This can either be an initial request or
    a refresh request."""
    payload = _get_token_payload(strava_auth, refresh=refresh)

    response = requests.post(ACCESS_TOKEN_URL, data=payload)

    if response.status_code != 200:
        logger.error(f"Token request failed {response.status_code}.")
        logger.error(f'Errors: {response.content.decode("utf-8")}')
        return

    strava_token_response = StravaTokenResponse(**response.json())
    logger.info(f"StravaTokenReponse: {strava_token_response}")
    strava_auth.update_token(strava_token_response)


def _get_token_payload(strava_auth: StravaAuthorization, refresh=False):
    """Creates the payload for a token request. Either initial or refresh."""
    if not settings.STRAVA_CLIENT_SECRET or not settings.STRAVA_CLIENT_ID:
        return

    payload = {
        "client_id": settings.STRAVA_CLIENT_ID,
        "client_secret": settings.STRAVA_CLIENT_SECRET,
    }

    if refresh:
        payload["refresh_token"] = strava_auth.refresh_token
        payload["grant_type"] = "refresh_token"
    else:
        payload["code"] = strava_auth.code
        payload["grant_type"] = "authorization_code"

    return payload


def save_auth(request):
    if "code" not in request.GET:
        logger.error("No code in request")
        return
    code = request.GET.get("code")
    scope = request.GET["scope"].split(",") if "scope" in request.GET else []

    StravaAuthorization.objects.filter(user=request.user).delete()

    strava_auth = StravaAuthorization.create_with_scope(
        user=request.user, code=code, scope_list=scope,
    )
    request_access_token(strava_auth)
