from extractor.models import Extractor
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from extractor.serializers import ExtractorSerializer


class ExtractorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Extractor.objects.all().order_by('-begin_date')
    serializer_class = ExtractorSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'type_audit']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type_audit', 'status_job']