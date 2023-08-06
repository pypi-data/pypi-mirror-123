import logging

from django.apps import apps
from django.contrib import admin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

logger = logging.getLogger(__name__)

from ob_dj_factorial.core.factorial.models import FHEmployee, FHOAuth, FHTeam


@admin.register(FHOAuth)
class FHOAuthAdmin(admin.ModelAdmin):
    list_display = ("site", "expires_in", "hs_action")
    change_list_template = "admin_oauth_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("add-oauth/", self.add_oauth),
        ]
        return my_urls + urls

    def add_oauth(self, request):
        return HttpResponseRedirect(self.hs_oauth_link())

    @staticmethod
    def hs_oauth_link() -> str:
        return apps.get_app_config("factorial").get_oauth_link()

    def hs_action(self, obj):
        return format_html(
            '<a class="button" href="{}">Sync Data</a> '
            '<a class="button" href="{}">Refresh Tokens</a>',
            reverse("factorial-admin:sync_all"),
            apps.get_app_config("factorial").get_oauth_link(),
        )

    hs_action.short_description = "Factorial: OAuth"
    hs_action.allow_tags = True

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


@admin.register(FHEmployee)
class FHEmployeeAdmin(admin.ModelAdmin,):
    list_display = ["email", "full_name", "employee_id", "teams"]

    def teams(self, obj):
        return ", ".join(obj.teams.all().values_list("team__name", flat=True))


@admin.register(FHTeam)
class FHTeamAdmin(admin.ModelAdmin,):
    list_display = [
        "name",
        # "leads"
    ]
