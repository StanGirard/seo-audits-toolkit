from django_filters.rest_framework import DjangoFilterBackend
from org.models import Website
from organizations.views.mixins import (MembershipRequiredMixin,
                                        OrganizationMixin)
from rest_framework import filters, permissions, viewsets

from .serializers import BertSerializer
from .models import Bert

## https://docs.djangoproject.com/en/3.1/topics/http/views/
class BertViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to summarize text
    GPU needed for better performance
    """

    ## User has to be authenticated
    permission_classes = [permissions.IsAuthenticated]

    ## Serializer defines how we respond to REST request
    serializer_class = BertSerializer

    ## Which filtering backends we want to us. 
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['status_job']
    ordering_fields = ['id', 'begin_date']
    
    ## Filters the result so that we only get the results for the user making the request.
    def get_queryset(self):
        return Bert.objects.for_user(self.request.user).order_by('-begin_date')
