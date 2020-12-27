from django.db import models
# Create your models here.


class Yake(models.Model):
    text = models.TextField(blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    ngram = models.IntegerField()
    language = models.CharField(max_length=10)
    number_keywords = models.IntegerField()
    status_job = models.CharField(max_length=20,blank=True, null=True)
    task_id = models.CharField(max_length=50,blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)