from datetime import datetime

import pytz
from django.http import Http404
from django.utils import timezone
from org.models import Website
from rest_framework import serializers

from .models import Bert
from .tasks import bert_job


class BertSerializer(serializers.ModelSerializer):
    website_name = serializers.CharField(source='bert.name',write_only=True)
    website = serializers.ReadOnlyField()
    summary = serializers.CharField(read_only=True) 
    class Meta:
        model = Bert
        fields = ['id','website','website_name','summary','text', 'result', 'status_job', 'begin_date']
    def create(self, validated_data):
        org = Website.objects.filter(id=validated_data["bert"]["name"]).first()
        bert_task = bert_job.delay(validated_data["text"])
        newBert = Bert.objects.create(org=org,text = validated_data["text"],status_job="SCHEDULED",task_id=str(bert_task.id), result="", begin_date=timezone.now())
        return newBert