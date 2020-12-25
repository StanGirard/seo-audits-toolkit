from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from org.models import Website
from org.serializers import WebsiteSerializer


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
