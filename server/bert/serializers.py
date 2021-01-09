from datetime import datetime

import pytz
from django.http import Http404
from django.utils import timezone
from org.models import Website
from rest_framework import serializers

from .models import Bert
from .tasks import bert_job

## Serializers define how we interact with API calls.
## https://docs.djangoproject.com/en/3.1/topics/serialization/
class BertSerializer(serializers.ModelSerializer):
    ## Required for the front, we declare a write only field that contains the organization
    website_name = serializers.CharField(source='bert.name',write_only=True)
    
    ## Creation of a field that contains the website name. It uses the website method from the models.py
    website = serializers.ReadOnlyField()

    ## Creation of a field that contains a summary. it uses the summary method from the models.py
    summary = serializers.CharField(read_only=True) 
    class Meta:
        model = Bert

        ## Fields that we want in our API
        fields = ['id','website','website_name','summary','text', 'result', 'status_job', 'begin_date']
    
    # We overwrite the post default method to add custom logic
    def create(self, validated_data):
        ## We extract the organization from the POST Method
        org = Website.objects.filter(id=validated_data["bert"]["name"]).first()

        ## We launch a celery task without waiting for it to complete
        bert_task = bert_job.delay(validated_data["text"])
        
        newBert = Bert.objects.create(org=org,text = validated_data["text"],status_job="SCHEDULED",task_id=str(bert_task.id), result="", begin_date=timezone.now())
        return newBert