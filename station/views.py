from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from .serializers import StationSerializer
from .models import Station
from vehicle.models import Vehicle
from vehicle.serializers import VehicleSerializer
import logging

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


# Create your views here.
class StationView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        user = request.user
        data["owner"] = user.id
        if user.is_admin:
            serializer = StationSerializer(data=data)
            if serializer.is_valid():
                station = serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Don't have sufficient permission"}, status.HTTP_401_UNAUTHORIZED)

    @method_decorator(cache_page(3600))
    @method_decorator(vary_on_headers("Authorization", ))
    def get(self, request):
        """ Get all available vehicles in an station """
        try:
            station_id = request.GET.get("station_id")
            station = Station.objects.get(station_id=station_id)
            vehicles = Vehicle.objects.filter(station_id=station_id, status="available")

            station_serializer = StationSerializer(station)
            station_data = station_serializer.data
            station_data["vehicles"] = []
            vehicle_serializer = VehicleSerializer(vehicles, many=True)

            for veh in vehicle_serializer.data:
                station_data["vehicles"].append(dict(veh))
        except Exception as e:
            logging.error(str(e))
            return Response(data={"error": {"error": type(e).__name__, "message": str(e)}})
        return Response(data={"data": station_data}, status=status.HTTP_200_OK)
