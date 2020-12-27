from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Lighthouse, Lighthouse_Result
from .serializers import LighthouseResultSerializer, LighthouseSerializer


class LighthouseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    @action(methods=['get'], detail=True, serializer_class=LighthouseSerializer)    
    def test(self, request, pk=None):
        query = Lighthouse_Result.objects.filter(url=pk)
        return Response({"timesheet":"hello from getbydate"})

    queryset = Lighthouse.objects.all().order_by('-last_updated')
    serializer_class = LighthouseSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['url', 'last_updated']

    filterset_fields = ['url', 'scheduled']


class LighthouseResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Lighthouse_Result.objects.all().order_by('-timestamp')
    serializer_class = LighthouseResultSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['url', 'timestamp']
    filterset_fields = ['url']