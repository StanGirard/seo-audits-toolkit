from .models import Lighthouse,Lighthouse_Result
from rest_framework import serializers


class LighthouseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lighthouse_Result
        fields = ['id','result', 'timestamp']

class LighthouseSerializer(serializers.ModelSerializer):
    # lighthouse_results = LighthouseResultSerializer(many=True)
    lighthouse_results = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Lighthouse
        fields = ['id','url', 'scheduled', 'update_rate', 'lighthouse_results','last_updated']
