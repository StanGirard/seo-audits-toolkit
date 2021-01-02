from django.db import models
# Create your models here.
from django.utils import timezone
from org.models import Website

class ForUser(models.Manager):
    def for_user(self, user):
        org = Website.objects.filter(users=user)
        return self.get_queryset().filter(org__in=org.values_list('id', flat=True))


class Yake(models.Model):
    org = models.ForeignKey(Website, related_name='yake', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    ngram = models.IntegerField()
    name= models.CharField(max_length=20)
    language = models.CharField(max_length=10)
    number_keywords = models.IntegerField()
    status_job = models.CharField(max_length=20,blank=True, null=True)
    task_id = models.CharField(max_length=50,blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    objects = ForUser()
    
    @property
    def website(self):
        return self.org.name