from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from users.views import UserViewSet, GroupViewSet 
from extractor.views import ExtractorViewSet
from lighthouse.views import LighthouseViewSet, LighthouseResultViewSet
from keywords.views import KeywordsViewSet
from organizations.backends import invitation_backend

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'api/extractor', ExtractorViewSet,basename='Extractor')
router.register(r'api/lighthouse', LighthouseViewSet)
router.register(r'api/results', LighthouseResultViewSet)
router.register(r'api/keywords', KeywordsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('extractor/', include('extractor.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('organizations.urls')),
    path('invitations/', include(invitation_backend().get_urls()))
]