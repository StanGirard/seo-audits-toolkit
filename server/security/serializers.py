from rest_framework import serializers

from .models import Security, Security_Result
from .tasks import security_add_new_url_crawler
from org.models import Website

class SecurityResultSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)
    website_name = serializers.CharField(source='security_results_org.name',write_only=True)
    website = serializers.ReadOnlyField()
    class Meta:
        model = Security_Result
        fields = ['id','url', 'result','score', 'timestamp', 'website','website_name']


class SecuritySerializer(serializers.ModelSerializer):
    # security_results = SecurityResultSerializer(many=True)
    website_name = serializers.CharField(source='security.name',write_only=True)
    website = serializers.ReadOnlyField()
    class Meta:
        model = Security
        fields = ['id', 'url','website','website_name','score' ,'scheduled', 'last_updated']

    def create(self, validated_data):
        ## Creates the celery task
        
        org = Website.objects.filter(id=validated_data["security"]["name"]).first()

        ## Creates the Save to DB
        if (org.only_domain and org.url not in validated_data["url"]):
                raise serializers.ValidationError("Error in your message")
        else:
            scheduled = False
            if not "scheduled" in validated_data:
                scheduled = False
            else:
                scheduled = True
            security_runner = security_add_new_url_crawler.delay(validated_data["url"])
            new_security = Security.objects.create(
                org=org,
                url=validated_data["url"],
                scheduled= scheduled
            )
        
            return new_security