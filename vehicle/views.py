from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from .serializers import VehicleSerializer


# Create your views here.
class VehicleCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        user = request.user

        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            vehicle = serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
"""
from django.shortcuts import render, redirect
from .models import Vehicle

def available_vehicles(request, station_id):
    vehicles = Vehicle.objects.filter(station_id=station_id, status='available')
    return render(request, 'available_vehicles.html', {'vehicles': vehicles})

def pick_up_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.status = 'in_use'
    vehicle.save()
    return redirect('vehicle_details', vehicle_id=vehicle_id)

def vehicle_details(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    return render(request, 'vehicle_details.html', {'vehicle': vehicle})

def return_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.status = 'available'
    vehicle.save()
    return redirect('vehicle_details', vehicle_id=vehicle_id)
"""