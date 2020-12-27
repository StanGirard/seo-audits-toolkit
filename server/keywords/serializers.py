import json
from datetime import datetime

import pytz
from django.utils import timezone
from extractor.models import Extractor
from rest_framework import serializers

from .models import Yake
from .tasks import keywords_job


class KeywordsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Yake
        fields = ['id', 'text', 'result','ngram','language','number_keywords','status_job', 'task_id', 'last_updated' ]
        extra_kwargs = {
            'result': {'read_only': True},
            'status_job': {'read_only': True},
            'task_id': {'read_only': True},
            'last_updated': {'read_only': True},
        }
    def create(self, validated_data):
        ## Creates the celery task
        keywords_task = keywords_job.delay(validated_data["text"],validated_data["language"],validated_data["ngram"],validated_data["number_keywords"])
        
        ## Creates the Save to DB
        newKeyword = Yake.objects.create(
        text=validated_data["text"],
        status_job="SCHEDULED",
        ngram=validated_data["ngram"],
        language=validated_data["language"],
        number_keywords=validated_data["number_keywords"],
        task_id=str(keywords_task.id), 
        result="", 
        last_updated=timezone.now()
        )
        
        return newKeyword
