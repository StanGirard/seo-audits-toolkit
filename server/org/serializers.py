from datetime import datetime

import pytz
from django.utils import timezone
from rest_framework import serializers

from org.models import Website


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id','url', "name","only_domain"]
