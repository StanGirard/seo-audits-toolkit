from django_filters.rest_framework import DjangoFilterBackend
from org.models import Website
from organizations.views.mixins import (MembershipRequiredMixin,
                                        OrganizationMixin)
from rest_framework import filters, permissions, viewsets

from .serializers import BertSerializer
from .models import Bert

class BertViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = BertSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['status_job']
    ordering_fields = ['id', 'begin_date']
    
    def get_queryset(self):
        return Bert.objects.for_user(self.request.user).order_by('-begin_date')
