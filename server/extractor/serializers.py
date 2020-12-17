from extractor.models import Extractor
from rest_framework import serializers
from datetime import datetime
from .tasks import extractor_job
from .models import Extractor
from django.utils import timezone
import pytz

class ExtractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extractor
        fields = ['id','url', 'result', 'type_audit', 'status_job', 'begin_date']

    def create(self, validated_data):
        ## Creates the celery task
        extractor_task = extractor_job.delay(validated_data["url"],validated_data["type_audit"])
        
        ## Creates the Save to DB
        newExtractor = Extractor.objects.create(
        url = validated_data["url"],status_job="SCHEDULED",task_id=str(extractor_task.id), result="", begin_date=timezone.now(), type_audit=validated_data["type_audit"]
        )
        
        
        return newExtractor