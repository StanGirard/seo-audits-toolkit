from django.db import models
from organizations.models import Organization

# Create your models here.

class Website(Organization):
    url = models.CharField(max_length=200)
    only_domain = models.BooleanField(default=False)
