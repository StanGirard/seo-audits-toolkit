from django.db import models

# Create your models here.
class Lighthouse(models.Model): 
    url = models.CharField(max_length=200)
    update_rate = models.CharField(max_length=100)
    scheduled = models.BooleanField(default=False)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.url

class Lighthouse_Result(models.Model):
    url = models.ForeignKey(Lighthouse, on_delete=models.CASCADE)
    result = models.TextField(max_length=10)
    timestamp = models.DateTimeField(blank=True, null=True)