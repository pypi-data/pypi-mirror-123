from urllib.parse import urlencode

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import register
from django.utils.translation import gettext_lazy as _

from ob_dj_factorial.core.factorial import settings_validation


class FactorialConfig(AppConfig):
    name = "ob_dj_factorial.core.factorial"
    verbose_name = _("Factorial")

    @staticmethod
    def get_oauth_link():
        params = {
            "client_id": settings.FH_CLIENT_ID,
            "redirect_uri": settings.FH_REDIRECT_URI,
            # "scope": settings.FH_SCOPES,
            "response_type": "code",
        }
        return f"https://api.factorialhr.com/oauth/authorize?{urlencode(params)}"

    def ready(self):
        register(settings_validation.required_settings)
        register(settings_validation.required_dependencies)
        register(settings_validation.required_installed_apps)
