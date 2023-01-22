from django.db import models
import uuid

from authentication.models import User
from vehicle.models import Vehicle


# Create your models here.
class VehicleBooking(models.Model):
    booking_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="id")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, to_field="vehicle_id")
    booking_time = models.DateTimeField(auto_created=True, auto_now_add=True)
    booking_end_time = models.DateTimeField()  # For keeping track of next availability