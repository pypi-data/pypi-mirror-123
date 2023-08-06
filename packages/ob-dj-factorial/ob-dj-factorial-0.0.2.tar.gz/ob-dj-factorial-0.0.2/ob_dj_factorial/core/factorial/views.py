import logging

import requests
from celery import current_app
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from ob_dj_factorial.core.factorial.models import FHOAuth

logger = logging.getLogger(__name__)


class FactorialOAuthView(View):
    permissions: tuple = ("factorial.add_oauth",)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if "code" not in request.GET:
            raise Http404
        code = request.GET.get("code")

        site = Site.objects.get_current()

        response = requests.post(
            url=f"{settings.FH_API_BASE_URL}/oauth/token",
            data={
                "client_id": settings.FH_CLIENT_ID,
                "client_secret": settings.FH_CLIENT_SECRET,
                "redirect_uri": settings.FH_REDIRECT_URI,
                "grant_type": "authorization_code",
                "code": code,
            },
        )
        logger.debug(f"{response.content}")
        response.raise_for_status()
        logger.debug(
            f"{self.__class__.__name__}() Response "
            f"<url:{response.url}, "
            f"status_code:{response.status_code}>"
        )
        _r = response.json()

        try:
            oa = FHOAuth.objects.get(site=site)
            oa.access_token = _r.get("access_token")
            oa.refresh_token = _r.get("refresh_token")
            oa.expires_in = _r.get("expires_in")
            oa.save()
        except FHOAuth.DoesNotExist:
            oa = FHOAuth.objects.create(
                site=site,
                access_token=_r.get("access_token"),
                refresh_token=_r.get("refresh_token"),
                expires_in=_r.get("expires_in"),
            )

        # TODO: Post message in sessions to show success in admin
        #       messages https://docs.djangoproject.com/en/3.1/ref/contrib/messages/
        return redirect(reverse("admin:factorial_fhoauth_change", args=[oa.id,]))


class FactorialAllView(View):

    permissions: tuple = ("integrations.add_oauth",)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        site = Site.objects.get_current()

        instance = FHOAuth.objects.get(site=site)
        current_app.send_task("ob_dj_factorial.core.factorial.tasks.sync_all_objects",)

        return redirect(reverse("admin:factorial_fhoauth_change", args=[instance.id,]))
