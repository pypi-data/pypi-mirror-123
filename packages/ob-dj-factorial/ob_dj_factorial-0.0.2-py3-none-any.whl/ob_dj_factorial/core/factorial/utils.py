import logging
import typing

import requests
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from requests import Response

logger = logging.getLogger(__name__)


class FactorialClient:
    """ FactorialClient is the API Wrapper used for making calls and interacting with Factorial APIs
    """

    api = "https://api.factorialhr.com"

    def __init__(self, access_token: str):
        self.access_token = access_token

    def _authorization_header(self) -> str:
        return f"Bearer {self.access_token}"

    def _get_headers(
        self, content_type: typing.Optional[typing.Text] = None,
    ) -> typing.Dict:
        content_type = content_type or "application/json"
        header = {"Content-Type": content_type, "Accept": content_type}
        header.update({"Authorization": self._authorization_header()})

        return header

    @staticmethod
    def _make_request(
        url: typing.Text, method: typing.Text = "GET", **kwargs,
    ) -> Response:
        response = requests.request(method, url, **kwargs)
        logger.debug(f"<url:{response.url}, " f"status_code:{response.status_code}>,")
        if response.status_code != 200:
            logger.debug(f"response :{response.json()}")
        response.raise_for_status()
        return response

    def get_employees(self) -> typing.List:
        """GET https://api.factorialhr.com/api/v1/employees"""
        return self._make_request(
            f"{self.api}/api/v1/employees", headers=self._get_headers(),
        ).json()

    def get_teams(self) -> typing.List:
        """GET https://api.factorialhr.com/api/v1/teams"""
        return self._make_request(
            f"{self.api}/api/v1/teams", headers=self._get_headers(),
        ).json()


def django_admin_staff_permission_required(perm, login_url=None, raise_exception=True):
    """
    Decorator for views that checks whether a staff user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def check_perms(user):
        perms = (perm,) if isinstance(perm, str) else perm
        # First check if the user has the permission (even anon users)
        # Always the user must be is_staff True
        if user.has_perms(perms) and user.is_staff:
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False

    login_url = login_url or "admin:login"
    return user_passes_test(check_perms, login_url=login_url)
