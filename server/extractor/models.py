import datetime

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class Extractor(models.Model):
    extractor_type = models.TextChoices('Extractor', 'HEADERS IMAGES LINKS')
    url = models.CharField(max_length=200)
    result = JSONField(blank=True, null=True)
    type_audit = models.CharField(blank=True, choices=extractor_type.choices, max_length=20)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    status_job = models.CharField(max_length=30, blank=True, null=True)
    begin_date = models.DateTimeField(blank=True, null=True)

    def __repr__(self):
        return '<Audit {}>'.format(self.url)
