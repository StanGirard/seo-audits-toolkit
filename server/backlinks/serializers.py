from django.utils import timezone
from rest_framework import serializers

from org.models import Website

from .models import BacklinkAudit
from .tasks import backlinks_job


## Serializers define how we interact with API calls.
## https://docs.djangoproject.com/en/3.1/topics/serialization/
class BacklinksSerializer(serializers.ModelSerializer):
    ## Required for the front, we declare a write only field that contains the organization
    website_name = serializers.CharField(source='backlinkaudit.name', write_only=True)

    ## Creation of a field that contains the website name. It uses the website method from the models.py
    website = serializers.ReadOnlyField()

    class Meta:
        model = BacklinkAudit

        ## Fields that we want in our API
        fields = ['id', 'domain', 'website', 'website_name', 'result', 'status_job', 'last_updated']
        extra_kwargs = {
            'result': {'read_only': True},
            'status_job': {'read_only': True},
            'task_id': {'read_only': True},
            'last_updated': {'read_only': True},
        }

    # We overwrite the post default method to add custom logic
    def create(self, validated_data):
        ## We extract the organization from the POST Method
        org = Website.objects.filter(id=validated_data["backlinkaudit"]["name"]).first()

        ## Verifies if the organization allows other domains than itself
        if org.only_domain and org.url not in validated_data["domain"]:
            raise serializers.ValidationError("Error in your message")

        ## We launch a celery task without waiting for it to complete
        backlinks_task = backlinks_job.delay(validated_data["domain"])

        return BacklinkAudit.objects.create(
            org=org,
            domain=validated_data["domain"],
            status_job="SCHEDULED",
            task_id=str(backlinks_task.id),
            last_updated=timezone.now(),
        )
