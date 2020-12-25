from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Lighthouse, Lighthouse_Result
from .serializers import LighthouseResultSerializer, LighthouseSerializer


class LighthouseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Lighthouse.objects.all().order_by('-last_updated')
    serializer_class = LighthouseSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['url', 'last_updated']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['url','scheduled']

class LighthouseResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Lighthouse_Result.objects.all().order_by('-timestamp')
    serializer_class = LighthouseResultSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['url', 'timestamp']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['url']
