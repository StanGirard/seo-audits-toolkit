from datetime import datetime

import pytz
from django.http import Http404
from django.utils import timezone
from org.models import Website
from rest_framework import serializers

from extractor.models import Extractor

from .models import Extractor
from .tasks import extractor_job


class ExtractorSerializer(serializers.ModelSerializer):
    website_name = serializers.CharField(source='extractor.name',write_only=True)
    website = serializers.ReadOnlyField()

    class Meta:
        model = Extractor
        fields = ['id','website','website_name','url', 'result', 'type_audit', 'status_job', 'begin_date']
    def create(self, validated_data):

        
        ## Creates the celery task
        org = Website.objects.filter(id=validated_data["extractor"]["name"]).first()
        
        
        if (org.only_domain and org.url not in validated_data["url"]):
            raise serializers.ValidationError("Error in your message")
        else:
            extractor_task = extractor_job.delay(validated_data["url"],validated_data["type_audit"])
            newExtractor = Extractor.objects.create(org=org,
            url = validated_data["url"],status_job="SCHEDULED",task_id=str(extractor_task.id), result="", begin_date=timezone.now(), type_audit=validated_data["type_audit"]
            )
            return newExtractor
