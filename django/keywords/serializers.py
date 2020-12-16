from extractor.models import Extractor
from rest_framework import serializers
from datetime import datetime
from .tasks import keywords_job
from .models import Keyword
from django.utils import timezone
import pytz
import json

class KeywordsSerializer(serializers.ModelSerializer):
    # language = serializers.CharField(write_only=True)
    # ngram = serializers.IntegerField(write_only=True)
    # number = serializers.IntegerField(write_only=True)
    class Meta:
        model = Keyword
        fields = ['id', 'method', 'text', 'result','settings','status_job', 'task_id', 'last_updated' ]
        extra_kwargs = {
            'result': {'read_only': True},
            'status_job': {'read_only': True},
            'task_id': {'read_only': True},
            'last_updated': {'read_only': True},
        }
    def create(self, validated_data):
        ## Creates the celery task
        keywords_task = keywords_job.delay(validated_data["text"],validated_data["settings"]["language"],validated_data["settings"]["ngram"],validated_data["settings"]["number"])
        
        ## Creates the Save to DB
        newKeyword = Keyword.objects.create(
        method=validated_data["method"],
        text=validated_data["text"],
        status_job="SCHEDULED",
        settings=validated_data["settings"],
        task_id=str(keywords_task.id), 
        result="", 
        last_updated=timezone.now()
        )
        
        return newKeyword