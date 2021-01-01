import datetime

from django.db import models
from django.utils import timezone
from org.models import Website

class ForUser(models.Manager):
    def for_user(self, user):
        org = Website.objects.filter(users=user)
        return self.get_queryset().filter(org__in=org.values_list('id', flat=True))

class Bert(models.Model):
    org = models.ForeignKey(Website, related_name='website', on_delete=models.CASCADE)
    text = models.TextField()
    result = models.TextField(blank=True, null=True)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    status_job = models.CharField(max_length=30, blank=True, null=True)
    begin_date = models.DateTimeField(blank=True, null=True)

    objects = ForUser()
    

    def __repr__(self):
        return '<Bert {}>'.format(self.org)

    @property
    def website(self):
        return self.org.name
    
    @property
    def summary(self):
        return self.text[:200]