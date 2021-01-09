from datetime import datetime

import pytz
from django.utils import timezone
from rest_framework import serializers

from org.models import Website

## Serializers define how we interact with API calls.
## https://docs.djangoproject.com/en/3.1/topics/serialization/
class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website

        ## Fields that we want in our API
        fields = ['id','url', "name","only_domain"]
