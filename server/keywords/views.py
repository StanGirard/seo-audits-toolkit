from django_filters.rest_framework import DjangoFilterBackend
from org.models import Website
from rest_framework import filters, permissions, viewsets

from keywords.models import Yake
from keywords.serializers import KeywordsSerializer


class YakeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = KeywordsSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['id']
    filterset_fields = ['last_updated']

    def get_queryset(self):
        return Yake.objects.for_user(self.request.user).order_by('-last_updated')
