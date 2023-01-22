from django.db import models
import uuid

from station.models import Station


# Create your models here.
class Vehicle(models.Model):
    vehicle_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    company = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    STATUS_CHOICES = (('available', 'Available'), ('in_use', 'In Use'))
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, to_field="station_id")

    def __str__(self):
        return self.make + ' ' + self.model
