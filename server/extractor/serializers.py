from datetime import datetime

import pytz
from django.http import Http404
from django.utils import timezone
from org.models import Website
from rest_framework import serializers

from extractor.models import Extractor, Sitemap

from .models import Extractor
from .tasks import extractor_job, sitemap_job

## Serializers define how we interact with API calls.
## https://docs.djangoproject.com/en/3.1/topics/serialization/
class ExtractorSerializer(serializers.ModelSerializer):
    ## Required for the front, we declare a write only field that contains the organization
    website_name = serializers.CharField(source='extractor.name',write_only=True)
    ## Creation of a field that contains the website name. It uses the website method from the models.py
    website = serializers.ReadOnlyField()

    class Meta:
        model = Extractor

        ## Fields that we want in our API
        fields = ['id','website','website_name','url', 'result', 'type_audit', 'status_job', 'begin_date']
    
     # We overwrite the post default method to add custom logic
    def create(self, validated_data): 
        ## We extract the organization from the POST Method
        org = Website.objects.filter(id=validated_data["extractor"]["name"]).first()
        
        ## We check if the org allows the user to request for urls other than the org
        if (org.only_domain and org.url not in validated_data["url"]):
            raise serializers.ValidationError("Error in your message")
        else:
            ## We launch a celery task without waiting for it to complete
            extractor_task = extractor_job.delay(validated_data["url"],validated_data["type_audit"])
            newExtractor = Extractor.objects.create(org=org,
            url = validated_data["url"],status_job="SCHEDULED",task_id=str(extractor_task.id), result="", begin_date=timezone.now(), type_audit=validated_data["type_audit"]
            )
            return newExtractor


class SitemapSerializer(serializers.ModelSerializer):
    website_name = serializers.CharField(source='sitemap.name',write_only=True)
    website = serializers.ReadOnlyField()

    class Meta:
        model = Sitemap
        fields = ['id','website','website_name','url', 'result', 'status_job', 'begin_date']
    
    def create(self, validated_data):
        org = Website.objects.filter(id=validated_data["sitemap"]["name"]).first()
        
        if (org.only_domain and org.url not in validated_data["url"]):
            raise serializers.ValidationError("Error in your message")
        else:
            sitemap_task = sitemap_job.delay(validated_data["url"], org.id)
            newSitemap = Sitemap.objects.create(org=org,
            url = validated_data["url"],status_job="SCHEDULED",task_id=str(sitemap_task.id), result="", begin_date=timezone.now()
            )
            return newSitemap