from django.db import models
from org.models import Website


## Model Manager
## Only displays objects where the user is part of the organization. Required for RBAC.
class ForUser(models.Manager):
    def for_user(self, user):
        org = Website.objects.filter(users=user)
        return self.get_queryset().filter(org__in=org.values_list('id', flat=True))


class BacklinkAudit(models.Model):
    org = models.ForeignKey(Website, related_name='backlink_audits', on_delete=models.CASCADE)
    domain = models.CharField(max_length=253)
    result = models.JSONField(blank=True, null=True)
    status_job = models.CharField(max_length=20, blank=True, null=True)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    objects = ForUser()

    ## Returns the organization name
    @property
    def website(self):
        return self.org.name

    def __str__(self):
        return self.domain
