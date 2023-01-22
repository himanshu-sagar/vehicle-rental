from rest_framework import serializers
from .models import VehicleBooking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBooking
        fields = '__all__'