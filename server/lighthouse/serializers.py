from rest_framework import serializers

from .models import Lighthouse, Lighthouse_Result
from .tasks import lighthouse_add_new_url_crawler

class LighthouseResultSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)

    class Meta:
        model = Lighthouse_Result
        fields = ['id','url', 'performance_score', 'accessibility_score',
                  'best_practices_score', 'seo_score', 'pwa_score', 'timestamp']


class LighthouseSerializer(serializers.ModelSerializer):
    # lighthouse_results = LighthouseResultSerializer(many=True)
    class Meta:
        model = Lighthouse
        fields = ['id', 'url', 'scheduled', 'last_updated']

    def create(self, validated_data):
        ## Creates the celery task
        lighthouse_runner = lighthouse_add_new_url_crawler.delay(validated_data["url"])
        
        ## Creates the Save to DB
        new_lighthouse = Lighthouse.objects.create(
            url=validated_data["url"],
            scheduled=validated_data["scheduled"]
        )
        
        return new_lighthouse