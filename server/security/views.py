from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Security, Security_Result
from .serializers import SecurityResultSerializer, SecuritySerializer


class SecurityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = SecuritySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['url', 'last_updated']

    filterset_fields = ['url', 'scheduled']

    def get_queryset(self):
        return Security.objects.for_user(self.request.user).order_by('-last_updated')


class SecurityResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = SecurityResultSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['url', 'timestamp']
    filterset_fields = ['url']

    def get_queryset(self):
        return Security_Result.objects.for_user(self.request.user).order_by('-timestamp')