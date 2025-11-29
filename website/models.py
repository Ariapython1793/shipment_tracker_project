from django.db import models
from django.utils import timezone
from datetime import timedelta

class ContainerStatus(models.TextChoices):
    IN_TRANSIT = 'in_transit', 'In Transit'
    DELAYED = 'delayed', 'Delayed'
    ARRIVED = 'arrived', 'Arrived'

class Container(models.Model):
    container_number = models.CharField(max_length=20, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=ContainerStatus.choices, default=ContainerStatus.IN_TRANSIT)
    depart_time = models.DateTimeField()
    distance_km = models.PositiveIntegerField()
    avg_speed_kmh = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def eta(self):
        hours = self.distance_km / max(self.avg_speed_kmh, 1)
        return self.depart_time + timedelta(hours=hours)

    def is_delayed(self):
        return timezone.now() > self.eta() and self.status != ContainerStatus.ARRIVED

    def __str__(self):
        return f"{self.container_number} ({self.origin} → {self.destination})"
