from django.urls import path

from ob_dj_factorial.apis.factorial.views import CallBackView

app_name = "factorial"

urlpatterns = [
    path("", CallBackView.as_view(), name="callback",),
]
