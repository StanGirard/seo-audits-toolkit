from django.db import models
from org.models import Website

## Model Manager
## Only displays objects where the user is part of the organization. Required for RBAC.
class ForUser(models.Manager):
    def for_user(self, user):
        org = Website.objects.filter(users=user)
        return self.get_queryset().filter(org__in=org.values_list('id', flat=True))

# Create your models here.
class Lighthouse(models.Model): 
    org = models.ForeignKey(Website, related_name='ligthouse', on_delete=models.CASCADE)
    url = models.CharField(max_length=200, unique=True)
    scheduled = models.BooleanField(default=False)
    last_updated = models.DateTimeField(blank=True, null=True)

    objects = ForUser()

    ## Returns the organization name
    @property
    def website(self):
        return self.org.name

    def __str__(self):
        return self.url

class Lighthouse_Result(models.Model):
    org = models.ForeignKey(Website, related_name='ligthouse_results_org', on_delete=models.CASCADE)
    url = models.ForeignKey(Lighthouse, related_name='lighthouse_results', on_delete=models.CASCADE)
    performance_score = models.CharField(max_length=10)
    accessibility_score = models.CharField(max_length=10)
    best_practices_score =models.CharField(max_length=10)
    seo_score = models.CharField(max_length=10)
    pwa_score = models.CharField(max_length=10)
    timestamp = models.DateTimeField(blank=True, null=True)

    objects = ForUser()

    ## Returns the organization name
    @property
    def website(self):
        return self.org.name