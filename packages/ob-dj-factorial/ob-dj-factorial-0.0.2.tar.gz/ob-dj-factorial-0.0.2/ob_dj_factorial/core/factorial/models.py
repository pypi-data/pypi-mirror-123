import typing

from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt

from ob_dj_factorial.core.factorial.managers import (
    FHEmployeeManager,
    FHOAuthManager,
    FHTeamManager,
)


class BaseFHModel(models.Model):
    class Meta:
        abstract = True

    def mark_deleted(self) -> typing.NoReturn:
        self.deleted_at = now()
        self.save()
        # TODO: django model delete record signal


class FHOAuth(models.Model):

    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="factorial_oa"
    )
    refresh_token = encrypt(models.CharField(max_length=3000))
    access_token = encrypt(models.CharField(max_length=3000))
    expires_in = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    stale = models.BooleanField(default=False)

    objects = FHOAuthManager()

    class Meta:
        verbose_name = _("Factorial: OAuth")
        verbose_name_plural = _("Factorial: OAuth")

    def __str__(self) -> typing.Text:
        return f"<{self._meta.object_name} Pk={self.pk}>"

    def save(self, **kwargs) -> None:
        if not self.pk:
            try:
                if self.site:
                    pass
            except ObjectDoesNotExist:
                self.site = Site.objects.get_current()
        super().save(**kwargs)


class FHTeam(BaseFHModel, models.Model):
    oauth = models.ForeignKey(FHOAuth, on_delete=models.CASCADE)
    team_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)

    objects = FHTeamManager()

    class Meta:
        verbose_name = _("Factorial: Team")
        verbose_name_plural = _("Factorial: Teams")


class FHEmployee(BaseFHModel, models.Model):

    oauth = models.ForeignKey(FHOAuth, on_delete=models.CASCADE)
    employee_id = models.CharField(
        max_length=3000, unique=True, help_text=_("Unique employee ID from FactorialHR")
    )
    email = models.EmailField(null=True, blank=True)
    full_name = models.CharField(max_length=300, null=True, blank=True)
    employee_object = models.JSONField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = FHEmployeeManager()

    class Meta:
        verbose_name = _("Factorial: Employee")
        verbose_name_plural = _("Factorial: Employees")

    def __str__(self) -> typing.Text:
        return f"{self.employee_id}"


class FHTeamMember(BaseFHModel, models.Model):
    team = models.ForeignKey(FHTeam, on_delete=models.CASCADE, related_name="members")
    employee = models.ForeignKey(
        FHEmployee, on_delete=models.CASCADE, related_name="teams"
    )


class FHTeamLead(BaseFHModel, models.Model):
    lead = models.ForeignKey(FHTeam, on_delete=models.CASCADE, related_name="leads")
    employee = models.ForeignKey(
        FHEmployee, on_delete=models.CASCADE, related_name="teams_lead"
    )
