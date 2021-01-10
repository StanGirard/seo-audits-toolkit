from org.models import Website
from rest_framework import serializers

from .models import Security, Security_Result
from .tasks import security_add_new_url_crawler


## Serializers define how we interact with API calls.
## https://docs.djangoproject.com/en/3.1/topics/serialization/
class SecurityResultSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)
    
    ## Required for the front, we declare a write only field that contains the organization
    website_name = serializers.CharField(source='security_results_org.name',write_only=True)
    
    ## Creation of a field that contains the website name. It uses the website method from the models.py
    website = serializers.ReadOnlyField()
    class Meta:
        model = Security_Result
        ## Fields that we want in our API
        fields = ['id','url', 'result','score', 'timestamp', 'website','website_name']


class SecuritySerializer(serializers.ModelSerializer):
    ## Required for the front, we declare a write only field that contains the organization
    website_name = serializers.CharField(source='security.name',write_only=True)
    
    ## Creation of a field that contains the website name. It uses the website method from the models.py
    website = serializers.ReadOnlyField()
    class Meta:
        model = Security

        ## Fields that we want in our API
        fields = ['id', 'url','website','website_name','score' ,'scheduled', 'last_updated']

    # We overwrite the post default method to add custom logic
    def create(self, validated_data):
        # We extract the organization from the POST Method
        org = Website.objects.filter(id=validated_data["security"]["name"]).first()

        ## Verifies if the organization allows other urls than itself
        if (org.only_domain and org.url not in validated_data["url"]):
                raise serializers.ValidationError("Error in your message")
        else:
            scheduled = False
            if not "scheduled" in validated_data:
                scheduled = False
            else:
                scheduled = True
            
            ## We launch a celery task without waiting for it to complete
            security_runner = security_add_new_url_crawler.delay(validated_data["url"])
            new_security = Security.objects.create(
                org=org,
                url=validated_data["url"],
                scheduled= scheduled
            )
        
            return new_security
