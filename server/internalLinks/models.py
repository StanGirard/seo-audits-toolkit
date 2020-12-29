import datetime

from django.db import models
from django.utils import timezone
from org.models import Website


class InternalLinks(models.Model):
    url = models.CharField(max_length=200)
    result = models.JSONField(blank=True, null=True)
    maximum = models.IntegerField()
    task_id = models.CharField(max_length=50, blank=True, null=True)
    status_job = models.CharField(max_length=30, blank=True, null=True)
    begin_date = models.DateTimeField(blank=True, null=True)