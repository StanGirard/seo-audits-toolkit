from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from users.views import UserViewSet, GroupViewSet 
from extractor.views import ExtractorViewSet
from lighthouse.views import LighthouseViewSet, LighthouseResultViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'api/extractor', ExtractorViewSet)
router.register(r'api/lighthouse', LighthouseViewSet)
router.register(r'api/results', LighthouseResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('extractor/', include('extractor.urls')),
    path('admin/', admin.site.urls)
]