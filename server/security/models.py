from django.db import models
from org.models import Website


## Model Manager
## Only displays objects where the user is part of the organization. Required for RBAC.
class ForUser(models.Manager):
    def for_user(self, user):
        org = Website.objects.filter(users=user)
        return self.get_queryset().filter(org__in=org.values_list('id', flat=True))

class Security(models.Model): 
    org = models.ForeignKey(Website, related_name='security', on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
    score = models.CharField(max_length=20, null=True)
    scheduled = models.BooleanField(default=False)
    last_updated = models.DateTimeField(blank=True, null=True)

    objects = ForUser()

    ## Returns the organization name
    @property
    def website(self):
        return self.org.name

    def __str__(self):
        return self.url

class Security_Result(models.Model):
    org = models.ForeignKey(Website, related_name='security_results_org', on_delete=models.CASCADE)
    url = models.ForeignKey(Security, related_name='security_results', on_delete=models.CASCADE)
    score = models.CharField(max_length=20, null=True)
    result = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    objects = ForUser()

    ## Returns the organization name
    @property
    def website(self):
        return self.org.name
