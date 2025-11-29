# tracking/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ContainerViewSet

router = DefaultRouter()
router.register('containers', ContainerViewSet, basename='container')

urlpatterns = [
    path('', include(router.urls)),
]
