from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .models import BacklinkAudit
from .serializers import BacklinksSerializer
from .pagination import PageNumberWithPageSizePagination


## https://docs.djangoproject.com/en/3.1/topics/http/views/
## Don't forget to register the view inside core/urls.py
class BacklinksViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to run a RankParse backlink audit on a domain
    """

    pagination_class = PageNumberWithPageSizePagination

    ## User has to be authenticated
    permission_classes = [permissions.IsAuthenticated]

    ## Serializer defines how we respond to REST request
    serializer_class = BacklinksSerializer

    ## Which filtering backends we want to use.
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['domain', 'last_updated']
    filterset_fields = ['domain', 'last_updated']

    ## Filters the result so that we only get the results for the user making the request.
    def get_queryset(self):
        return BacklinkAudit.objects.for_user(self.request.user).order_by('-last_updated')
