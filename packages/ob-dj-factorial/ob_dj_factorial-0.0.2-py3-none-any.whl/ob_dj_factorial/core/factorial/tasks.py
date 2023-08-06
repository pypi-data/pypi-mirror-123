import logging

import requests
from celery import current_app, shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from ob_dj_factorial.core.factorial.models import FHEmployee, FHOAuth, FHTeam

logger = logging.getLogger(__name__)


@shared_task(name="ob_dj_factorial.core.factorial.tasks.refresh_all_tokens", bind=True)
def refresh_all_tokens(self) -> None:
    for oa in FHOAuth.objects.all():
        current_app.send_task(
            "ob_dj_factorial.core.factorial.tasks.refresh_access_token", args=[oa.id],
        )


@shared_task(
    name="ob_dj_factorial.core.factorial.tasks.refresh_access_token", bind=True
)
def refresh_access_token(self, oauth_id: int) -> None:
    oa = FHOAuth.objects.get(id=oauth_id)
    if oa.refresh_token and not oa.stale:
        # TODO: Move to Utils?
        response = requests.post(
            url=f"{settings.HS_API_BASE_URL}/oauth/token",
            data={
                "grant_type": "refresh_token",
                "client_id": settings.HS_CLIENT_ID,
                "client_secret": settings.HS_CLIENT_SECRET,
                "refresh_token": oa.refresh_token,
            },
        )
        response.raise_for_status()
        logger.debug(
            f"{self.__class__.__name__}() Response "
            f"<url:{response.url}, "
            f"status_code:{response.status_code}>"
        )
        _r = response.json()
        oa.access_token = _r["access_token"]
        oa.refresh_token = _r["refresh_token"]
        oa.expires_in = _r["expires_in"]
        oa.save()
        logger.debug(f"refresh_access_token response payload: {_r}")
    else:
        oa.stale = True
    oa.save()


@shared_task(
    name="ob_dj_factorial.core.factorial.tasks.sync_all_objects",
    max_retries=2,
    bind=True,
    autoretry_for=(ObjectDoesNotExist,),
    default_retry_delay=5,
)
def sync_all_objects(self):
    FHEmployee.objects.sync()
    FHTeam.objects.sync()
    return "Success"
