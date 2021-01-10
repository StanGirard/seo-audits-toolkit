import json
from datetime import datetime

import pytz
from django.utils import timezone
from extractor.models import Extractor
from rest_framework import serializers

from .models import InternalLinks
from .tasks import internal_links_job

## Serializers define how we interact with API calls.
## https://docs.djangoproject.com/en/3.1/topics/serialization/
class InternalLinksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InternalLinks
        fields = ['id', 'url', 'result',  'maximum', 'task_id', 'status_job', 'begin_date' ]
        extra_kwargs = {
            'result': {'read_only': True},
            'status_job': {'read_only': True},
            'task_id': {'read_only': True},
            'begin_date': {'read_only': True},
        }
    def create(self, validated_data):
        ## Creates the celery task
        internal_links_task = internal_links_job.delay(validated_data["url"],validated_data["maximum"])
        
        ## Creates the Save to DB
        newInternal = InternalLinks.objects.create(
        url=validated_data["url"],
        maximum=validated_data["maximum"],
        status_job="SCHEDULED",
        task_id=str(internal_links_task.id),
        begin_date=timezone.now()
        )
        
        return newInternal
