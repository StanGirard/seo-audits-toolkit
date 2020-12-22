from org.models import Website
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from org.serializers import WebsiteSerializer
from rest_framework import permissions

class WebsiteViewSet(viewsets.ModelViewSet):
    
    
    serializer_class = WebsiteSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['url']
    ordering_fields = ['id', 'url']
    
    def get_queryset(self):
        org = Website.objects.filter(users=self.request.user)
        return org
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]