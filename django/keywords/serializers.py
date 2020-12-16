from extractor.models import Extractor
from rest_framework import serializers
from datetime import datetime
from .tasks import keywords_job
from .models import Keyword
from django.utils import timezone
import pytz

class KeywordsSerializer(serializers.ModelSerializer):
    language = serializers.CharField(write_only=True)
    ngram = serializers.IntegerField(write_only=True)
    number = serializers.IntegerField(write_only=True)
    class Meta:
        model = Keyword
        fields = ['id', 'method', 'text', 'result','settings','language','ngram','number','status_job', 'task_id', 'last_updated' ]
        extra_kwargs = {
            'result': {'read_only': True},
            'status_job': {'read_only': True},
            'task_id': {'read_only': True},
            'last_updated': {'read_only': True},
            'settings': {'read_only': True}
        }
    def create(self, validated_data):
        ## Creates the celery task
        settings = {"language": validated_data["language"], "ngram": validated_data["ngram"], "number":validated_data["number"]}
        keywords_task = keywords_job.delay(validated_data["text"],validated_data["language"],validated_data["ngram"],validated_data["number"])
        
        ## Creates the Save to DB
        newKeyword = Keyword.objects.create(
        method=validated_data["method"],
        text=validated_data["text"],
        status_job="SCHEDULED",
        settings=settings,
        task_id=str(keywords_task.id), 
        result="", 
        last_updated=timezone.now()
        )
        
        return newKeyword