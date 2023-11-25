import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from .authorization import get_authorization_url, STRAVA_AUTH_URL, request_access_token
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


def strava_callback(request):
    if "code" not in request.GET:
        logger.error("No code in request")
        return
    code = request.GET.get("code")
    scope = request.GET["scope"].split(",") if "scope" in request.GET else []

    StravaAuthorization.objects.filter(user=request.user).delete()

    strava_auth = StravaAuthorization.create_with_scope(
        user=request.user,
        code=code,
        scope_list=scope,
    )
    request_access_token(strava_auth)
    return HttpResponse("Strava authorization successful!")

