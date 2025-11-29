# tracking/api_views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Container
from .serializers import ContainerSerializer

class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all().order_by('-created_at')
    serializer_class = ContainerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'origin', 'destination']
    search_fields = ['container_number', 'origin', 'destination']

    def get_serializer(self, *args, **kwargs):
        # Inject dynamic fields (eta, is_delayed)
        serializer = super().get_serializer(*args, **kwargs)
        return serializer
