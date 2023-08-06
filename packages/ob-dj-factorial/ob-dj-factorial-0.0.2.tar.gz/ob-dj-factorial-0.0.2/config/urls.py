from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "factorial/",
        include("ob_dj_factorial.apis.factorial.urls", namespace="factorial"),
    ),
]
