import json
from datetime import datetime

import pytz
from django.utils import timezone
from extractor.models import Extractor
from rest_framework import serializers
from org.models import Website

from .models import Yake
from .tasks import keywords_job

## Serializers define how we interact with API calls.
## https://docs.djangoproject.com/en/3.1/topics/serialization/

class KeywordsSerializer(serializers.ModelSerializer):
    ## Required for the front, we declare a write only field that contains the organization
    website_name = serializers.CharField(source='yake.name',write_only=True)
    
    ## Creation of a field that contains the website name. It uses the website method from the models.py
    website = serializers.ReadOnlyField()
    class Meta:
        model = Yake
        
        ## Fields that we want in our API
        fields = ['id', 'text', 'website_name', 'website','name','result','ngram','language','number_keywords','status_job', 'last_updated' ]
        extra_kwargs = {
            'result': {'read_only': True},
            'status_job': {'read_only': True},
            'task_id': {'read_only': True},
            'last_updated': {'read_only': True},
        }
    
    # We overwrite the post default method to add custom logic
    def create(self, validated_data):
        ## We extract the organization from the POST Method
        org = Website.objects.filter(id=validated_data["yake"]["name"]).first()
        
        ## Verify if organization settings allow urls other than itself
        if (org.only_domain and org.url not in validated_data["url"]):
            raise serializers.ValidationError("Error in your message")
        
        else:
            ## We launch a celery task without waiting for it to complete
            keywords_task = keywords_job.delay(validated_data["text"],validated_data["language"],validated_data["ngram"],validated_data["number_keywords"])
            
            ## Creates the Save to DB
            newKeyword = Yake.objects.create(
            org= org,
            text=validated_data["text"],
            status_job="SCHEDULED",
            name=validated_data["name"],
            ngram=validated_data["ngram"],
            language=validated_data["language"],
            number_keywords=validated_data["number_keywords"],
            task_id=str(keywords_task.id), 
            result="", 
            last_updated=timezone.now()
            )
            
            return newKeyword
