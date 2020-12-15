from django.urls import path
from . import views

app_name = 'extractor'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:extractor_id>/', views.detail, name='detail'),
    path('headers/', views.headers_vote, name='extract_headers')
]
