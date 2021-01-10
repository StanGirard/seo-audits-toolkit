from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Security, Security_Result
from .serializers import SecurityResultSerializer, SecuritySerializer


class SecurityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view security
    """

    ## User has to be authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    ## Serializer defines how we respond to REST request
    serializer_class = SecuritySerializer
    
    ## Which filtering backends we want to use. 
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['url', 'last_updated']
    filterset_fields = ['url', 'scheduled']

    ## Filters the result so that we only get the results for the user making the request.
    def get_queryset(self):
        return Security.objects.for_user(self.request.user).order_by('-last_updated')


class SecurityResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view security results
    """

    ## User has to be authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    ## Serializer defines how we respond to REST request
    serializer_class = SecurityResultSerializer
    
    ## Which filtering backends we want to use. 
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['url', 'timestamp']
    filterset_fields = ['url']

    ## Filters the result so that we only get the results for the user making the request.
    def get_queryset(self):
        return Security_Result.objects.for_user(self.request.user).order_by('-timestamp')