from rest_framework import serializers

from .models import Lighthouse, Lighthouse_Result
from .tasks import lighthouse_add_new_url_crawler
from org.models import Website
class LighthouseResultSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)
    website_name = serializers.CharField(source='ligthouse_results_org.name',write_only=True)
    website = serializers.ReadOnlyField()
    class Meta:
        model = Lighthouse_Result
        fields = ['id','url', 'performance_score', 'accessibility_score',
                  'best_practices_score', 'seo_score', 'pwa_score', 'timestamp', 'website','website_name']


class LighthouseSerializer(serializers.ModelSerializer):
    # lighthouse_results = LighthouseResultSerializer(many=True)
    website_name = serializers.CharField(source='ligthouse.name',write_only=True)
    website = serializers.ReadOnlyField()
    class Meta:
        model = Lighthouse
        fields = ['id', 'url','website','website_name' ,'scheduled', 'last_updated']

    def create(self, validated_data):
        ## Creates the celery task
        
        org = Website.objects.filter(id=validated_data["ligthouse"]["name"]).first()

        ## Creates the Save to DB
        if (org.only_domain and org.url not in validated_data["url"]):
                raise serializers.ValidationError("Error in your message")
        else:
            scheduled = False
            if not "scheduled" in validated_data:
                scheduled = False
            else:
                scheduled = True
            lighthouse_runner = lighthouse_add_new_url_crawler.delay(validated_data["url"])
            new_lighthouse = Lighthouse.objects.create(
                org=org,
                url=validated_data["url"],
                scheduled= scheduled
            )
        
            return new_lighthouse