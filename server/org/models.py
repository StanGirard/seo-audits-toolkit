from django.db import models
from organizations.models import Organization

## Model Manager
## Only displays objects where the user is part of the organization. Required for RBAC.
class Website(Organization):
    url = models.CharField(max_length=200)
    only_domain = models.BooleanField(default=False)
    ## Only domain is an option that restricts the url of other models to just the one of your organization