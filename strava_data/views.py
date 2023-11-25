import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy

from .authorization import (
    get_authorization_url,
    STRAVA_AUTH_URL,
    request_access_token,
    save_auth,
)
from .models import StravaAuthorization

logger = logging.getLogger(__name__)


@login_required(login_url=reverse_lazy("login"))
def strava_authorize(request):
    http_host = request.META["HTTP_HOST"]

    authorization_url = get_authorization_url(http_host=http_host)

    context = {}
    if authorization_url:
        context["authorization_url"] = authorization_url
    else:
        logger.error(
            request,
            "Something went wrong with the authorization. "
            "Please contact the administrator.",
        )

    return render(request, "strava_auth.html", context=context)


@login_required(login_url=reverse_lazy("login"))
def save_strava_auth(request):
    if request.method == "GET" and "code" in request.GET:
        save_auth(request)
        return HttpResponse("Strava authorization successful!")
    elif request.method == "GET" and "error" in request.GET:
        if request.GET["error"] == "access_denied":
            logger.warning("User denied access")
            HttpResponse("User denied access")
    else:
        return Http404("Not found")
