from django_filters.rest_framework import DjangoFilterBackend
from org.models import Website
from organizations.views.mixins import (MembershipRequiredMixin,
                                        OrganizationMixin)
from rest_framework import filters, permissions, viewsets

from extractor.models import Extractor
from extractor.serializers import ExtractorSerializer


class ExtractorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = ExtractorSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['type_audit', 'status_job']
    ordering_fields = ['id', 'type_audit', 'begin_date']
    
    def get_queryset(self):
        return Extractor.objects.for_user(self.request.user).order_by('-begin_date')
