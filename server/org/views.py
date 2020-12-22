from org.models import Website
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from org.serializers import WebsiteSerializer
from rest_framework import permissions

class WebsiteViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['url']
    ordering_fields = ['id', 'url']
    
    # def get_queryset(self):
    #     return Extractor.objects.for_user(self.request.user).order_by('-begin_date')