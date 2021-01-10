from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from org.models import Website
from org.serializers import WebsiteSerializer


## https://docs.djangoproject.com/en/3.1/topics/http/views/
## Don't forget to register the view inside core/urls.py
class WebsiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to manage organizations
    """
    ## Serializer defines how we respond to REST request
    serializer_class = WebsiteSerializer
    
    ## Which filtering backends we want to use. 
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['url']
    ordering_fields = ['id', 'url']
    
    ## Filters the result so that we only get the results for the user making the request.
    def get_queryset(self):
        org = Website.objects.filter(users=self.request.user)
        return org
    
    ## Only admin user can create and delete organizations
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
