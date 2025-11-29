
# tracking/admin.py
from django.contrib import admin
from .models import Container

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('container_number', 'origin', 'destination', 'status', 'depart_time', 'distance_km', 'avg_speed_kmh')
    list_filter = ('status', 'origin', 'destination')
    search_fields = ('container_number', 'origin', 'destination')
