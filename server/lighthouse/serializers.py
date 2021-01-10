from org.models import Website
from rest_framework import serializers

from .models import Lighthouse, Lighthouse_Result
from .tasks import lighthouse_add_new_url_crawler


## Serializers define how we interact with API calls.
## https://docs.djangoproject.com/en/3.1/topics/serialization/
class LighthouseResultSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)
    
    ## Required for the front, we declare a write only field that contains the organization
    website_name = serializers.CharField(source='ligthouse_results_org.name',write_only=True)
    
    ## Creation of a field that contains the website name. It uses the website method from the models.py
    website = serializers.ReadOnlyField()
    class Meta:
        model = Lighthouse_Result

        ## Fields that we want in our API
        fields = ['id','url', 'performance_score', 'accessibility_score',
                  'best_practices_score', 'seo_score', 'pwa_score', 'timestamp', 'website','website_name']


class LighthouseSerializer(serializers.ModelSerializer):
    
    ## Required for the front, we declare a write only field that contains the organization
    website_name = serializers.CharField(source='ligthouse.name',write_only=True)
    
    ## Creation of a field that contains the website name. It uses the website method from the models.py
    website = serializers.ReadOnlyField()
    class Meta:
        model = Lighthouse
        fields = ['id', 'url','website','website_name' ,'scheduled', 'last_updated']

    # We overwrite the post default method to add custom logic
    def create(self, validated_data):
        ## We extract the organization from the POST Method
        org = Website.objects.filter(id=validated_data["ligthouse"]["name"]).first()

        ## Verifies if the organization allows urls other than itself
        if (org.only_domain and org.url not in validated_data["url"]):
                raise serializers.ValidationError("Error in your message")
        else:
            scheduled = False
            if not "scheduled" in validated_data:
                scheduled = False
            else:
                scheduled = True
            ## We launch a celery task without waiting for it to complete
            lighthouse_runner = lighthouse_add_new_url_crawler.delay(validated_data["url"])
            new_lighthouse = Lighthouse.objects.create(
                org=org,
                url=validated_data["url"],
                scheduled= scheduled
            )
        
            return new_lighthouse
