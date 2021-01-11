from django_filters.rest_framework import DjangoFilterBackend
from org.models import Website
from organizations.views.mixins import (MembershipRequiredMixin,
                                        OrganizationMixin)
from rest_framework import filters, permissions, viewsets

from extractor.models import Extractor, Sitemap
from extractor.serializers import ExtractorSerializer, SitemapSerializer
from .pagination import PageNumberWithPageSizePagination


## https://docs.djangoproject.com/en/3.1/topics/http/views/
## Don't forget to register the view inside core/urls.py
class ExtractorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to extract information about a webpage
    """
    pagination_class = PageNumberWithPageSizePagination
    ## User has to be authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    ## Serializer defines how we respond to REST request
    serializer_class = ExtractorSerializer
    
    ## Which filtering backends we want to us. 
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['type_audit', 'status_job']
    ordering_fields = ['begin_date']
    
    ## Filters the result so that we only get the results for the user making the request.
    def get_queryset(self):
        return Extractor.objects.for_user(self.request.user).order_by('-begin_date')

class SitemapViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users extract urls from a sitemap
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SitemapSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['url', 'status_job']
    ordering_fields = ['begin_date']
    
    def get_queryset(self):
        return Sitemap.objects.for_user(self.request.user).order_by('-begin_date')
