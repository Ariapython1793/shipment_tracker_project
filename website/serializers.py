# tracking/serializers.py
from rest_framework import serializers
from .models import Container

class ContainerSerializer(serializers.ModelSerializer):
    eta = serializers.DateTimeField(read_only=True)
    is_delayed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Container
        fields = ['id', 'container_number', 'origin', 'destination', 'status', 'depart_time',
                  'distance_km', 'avg_speed_kmh', 'eta', 'is_delayed']
