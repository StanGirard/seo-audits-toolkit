from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from keywords.models import Keyword
from keywords.serializers import KeywordsSerializer


class KeywordsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Keyword.objects.all().order_by('-last_updated')
    serializer_class = KeywordsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'method']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['method', 'last_updated']
