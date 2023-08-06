from django.urls import path

from ob_dj_factorial.core.factorial import views
from ob_dj_factorial.core.factorial.utils import django_admin_staff_permission_required

app_name = "factorial-admin"

urlpatterns = [
    path(
        "oauth",
        django_admin_staff_permission_required(views.FactorialOAuthView.permissions)(
            views.FactorialOAuthView.as_view()
        ),
        name="oauth",
    ),
    path(
        "sync-all",
        django_admin_staff_permission_required(views.FactorialAllView.permissions)(
            views.FactorialAllView.as_view()
        ),
        name="sync_all",
    ),
]
