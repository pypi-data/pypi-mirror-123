import logging
import typing

from celery import current_app
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from ob_dj_factorial.core.factorial.utils import FactorialClient

logger = logging.getLogger(__name__)


class BaseHSManager(models.Manager):
    def create(self, *args: typing.Any, **kwargs: typing.Any):
        if "oauth" not in kwargs:
            kwargs["oauth"] = self.get_oauth()
        return super().create(*args, **kwargs)

    def get_oauth(self) -> typing.Any:
        oauth = self.model.oauth.field.related_model
        return oauth.objects.get(site=Site.objects.get_current())


class FHOAuthManager(models.Manager):
    def create(self, **kwargs):
        instance = super().create(**kwargs)
        current_app.send_task(
            "ob_dj_factorial.core.factorial.tasks.sync_all_objects", countdown=5
        )
        return instance


class FHEmployeeManager(BaseHSManager):
    def sync(self):
        oauth = self.get_oauth()
        factorial = FactorialClient(access_token=oauth.access_token)
        for employee in factorial.get_employees():
            try:
                instance = self.get(employee_id=employee.get("id"))
                instance.employee_object = employee
                instance.full_name = employee.get("full_name")
                instance.email = employee.get("email")
                instance.save()
            except ObjectDoesNotExist:
                self.create(
                    employee_id=employee.get("id"),
                    full_name=employee.get("full_name"),
                    email=employee.get("email"),
                    employee_object=employee,
                )


class FHTeamManager(BaseHSManager):
    def sync(self):
        oauth = self.get_oauth()
        factorial = FactorialClient(access_token=oauth.access_token)
        for team in factorial.get_teams():
            try:
                instance = self.get(team_id=team.get("id"))
                instance.name = team.get("name")
                instance.save()
            except ObjectDoesNotExist:
                instance = self.create(team_id=team.get("id"), name=team.get("name"))
            # sync team members
            team_members_class = self.model.members.rel.related_model
            employee_class = team_members_class.employee.field.related_model
            for member in team.get("employee_ids"):
                employee = employee_class.objects.get(employee_id=member)
                team_members_class.objects.filter(employee=employee).delete()
                team_members_class.objects.create(team=instance, employee=employee)
            lead_members_class = self.model.leads.rel.related_model
            # sync team leads
            for lead in team.get("lead_ids"):
                employee = employee_class.objects.get(employee_id=lead)
                lead_members_class.objects.filter(employee=employee).delete()
                lead_members_class.objects.create(
                    lead=instance, employee=employee_class.objects.get(employee_id=lead)
                )
