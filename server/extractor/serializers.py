from extractor.models import Extractor
from rest_framework import serializers
from datetime import datetime
from .tasks import extractor_job
from .models import Extractor
from django.utils import timezone
import pytz
from org.models import Website
class ExtractorSerializer(serializers.ModelSerializer):
    website_name = serializers.CharField(source='extractor.url',write_only=True)
    class Meta:
        model = Extractor
        fields = ['id','website_name','url', 'result', 'type_audit', 'status_job', 'begin_date']
    def create(self, validated_data):
        ## Creates the celery task
        print("HELLO")
        extractor_task = extractor_job.delay(validated_data["url"],validated_data["type_audit"])
        print(validated_data)
        org = Website.objects.filter(url=validated_data["extractor"]["url"]).first()
        ## Creates the Save to DB
        
        newExtractor = Extractor.objects.create(org=org,
        url = validated_data["url"],status_job="SCHEDULED",task_id=str(extractor_task.id), result="", begin_date=timezone.now(), type_audit=validated_data["type_audit"]
        )
        
        
        return newExtractor
