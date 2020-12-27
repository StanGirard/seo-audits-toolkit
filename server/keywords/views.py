from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from keywords.models import Yake
from keywords.serializers import KeywordsSerializer


class YakeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Yake.objects.all().order_by('-last_updated')
    serializer_class = KeywordsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_updated']
