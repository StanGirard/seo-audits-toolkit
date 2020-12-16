from extractor.models import Extractor
from rest_framework import serializers
from datetime import datetime
from .tasks import keywords_job
from .models import Keyword
from django.utils import timezone
import pytz

class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'method', 'text', 'result', 'language', 'ngram','number','status_job', 'task_id', 'last_updated' ]

    def create(self, validated_data):
        ## Creates the celery task
        keywords_task = keywords_job.delay(validated_data["text"],validated_data["language"],validated_data["ngram"],validated_data["number"])
        
        ## Creates the Save to DB
        newKeyword = Keyword.objects.create(
        method=validated_data["method"],
        text=validated_data["text"],
        language=validated_data["language"],
        ngram=validated_data["ngram"],
        number=validated_data["number"],
        status_job="SCHEDULED",
        task_id=str(keywords_task.id), 
        result="", 
        last_updated=timezone.now()
        )
        
        return newKeyword