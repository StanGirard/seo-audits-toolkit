from rest_framework import serializers
from datetime import datetime
from django.utils import timezone
import pytz
from org.models import Website

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id','url', "name"]