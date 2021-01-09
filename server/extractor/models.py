import datetime

from django.db import models
from django.utils import timezone
from org.models import Website

## Model Manager
## Only displays objects where the user is part of the organization. Required for RBAC.

class ForUser(models.Manager):
    def for_user(self, user):
        org = Website.objects.filter(users=user)
        return self.get_queryset().filter(org__in=org.values_list('id', flat=True))

class Extractor(models.Model):
    org = models.ForeignKey(Website, related_name='extractor', on_delete=models.CASCADE)
    extractor_type = models.TextChoices('Extractor', 'HEADERS IMAGES LINKS')
    url = models.CharField(max_length=200)
    result = models.JSONField(blank=True, null=True)
    type_audit = models.CharField(blank=True, choices=extractor_type.choices, max_length=20)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    status_job = models.CharField(max_length=30, blank=True, null=True)
    begin_date = models.DateTimeField(blank=True, null=True)

    objects = ForUser()
    

    def __repr__(self):
        return '<Audit {}>'.format(self.url)
    
    ## Returns the organization name
    @property
    def website(self):
        return self.org.name

class Sitemap(models.Model):
    org = models.ForeignKey(Website, related_name='sitemap', on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
    result = models.JSONField(blank=True, null=True)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    status_job = models.CharField(max_length=30, blank=True, null=True)
    begin_date = models.DateTimeField(blank=True, null=True)

    objects = ForUser()

    ## Returns the organization name
    @property
    def website(self):
        return self.org.name
