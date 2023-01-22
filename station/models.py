from django.db import models
import uuid
from authentication.models import User


# Create your models here.
class Station(models.Model):
    station_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, to_field="id")

    def __str__(self):
        return self.name