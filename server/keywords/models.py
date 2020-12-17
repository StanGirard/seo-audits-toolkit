from django.db import models
# Create your models here.


class Keyword(models.Model):
    method = models.TextChoices('METHOD', 'YAKE')
    method = models.CharField(choices=method.choices, max_length=20)
    text = models.TextField(blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    settings = models.JSONField(blank=True, null=True)
    status_job = models.CharField(max_length=20,blank=True, null=True)
    task_id = models.CharField(max_length=50,blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)