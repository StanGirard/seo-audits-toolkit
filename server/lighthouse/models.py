from django.db import models

# Create your models here.
class Lighthouse(models.Model): 
    url = models.CharField(max_length=200, unique=True)
    scheduled = models.BooleanField(default=False)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.url

class Lighthouse_Result(models.Model):
    url = models.ForeignKey(Lighthouse, related_name='lighthouse_results', on_delete=models.CASCADE)
    performance_score = models.CharField(max_length=10)
    accessibility_score = models.CharField(max_length=10)
    best_practices_score =models.CharField(max_length=10)
    seo_score = models.CharField(max_length=10)
    pwa_score = models.CharField(max_length=10)
    timestamp = models.DateTimeField(blank=True, null=True)