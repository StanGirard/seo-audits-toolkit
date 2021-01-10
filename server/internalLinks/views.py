from internalLinks.serializers import InternalLinksSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .models import InternalLinks
from .serializers import InternalLinksSerializer


class InternalLinksViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = InternalLinks.objects.all().order_by('-begin_date')
    serializer_class = InternalLinksSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['begin_date']
