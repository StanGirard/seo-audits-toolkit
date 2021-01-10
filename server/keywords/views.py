from django_filters.rest_framework import DjangoFilterBackend
from org.models import Website
from rest_framework import filters, permissions, viewsets

from keywords.models import Yake
from keywords.serializers import KeywordsSerializer

## https://docs.djangoproject.com/en/3.1/topics/http/views/
## Don't forget to register the view inside core/urls.py
class YakeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to extract keywords
    """
    
    ## User has to be authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    ## Serializer defines how we respond to REST request
    serializer_class = KeywordsSerializer
    
    ## Which filtering backends we want to use. 
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['id']
    filterset_fields = ['last_updated']

    ## Filters the result so that we only get the results for the user making the request.
    def get_queryset(self):
        return Yake.objects.for_user(self.request.user).order_by('-last_updated')
