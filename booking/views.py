from rest_framework.views import APIView, Response, status
from vehicle.qr_code import QrCode
from rest_framework.permissions import IsAuthenticated
from vehicle.models import Vehicle
from booking.models import VehicleBooking
from booking.serializers import BookingSerializer
import logging
# Create your views here.


class VehicleBookingView(APIView):
    """
    Scan QR code image and decode to get vehicle_id, then book that vehicle for that user
    """
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            qrcode = QrCode()
            data = request.data

            vehicle_id = qrcode.decode_qr_code(data["qr_code_path"])

            logging.info("QR code decoded")
            vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
            if vehicle.status == 'in_use':
                return Response(
                    data={"error": {
                        "message": "Vehicle is not available for booking"
                    }},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            user = request.user
            booking_data = {
                "user": user.id,
                "vehicle": vehicle.vehicle_id,
                "booking_end_time": data.get("booking_end_time")
            }
            booking_serializer = BookingSerializer(data=booking_data)

            if booking_serializer.is_valid():
                booking_serializer.save()  # booking successful

                logging.info("Booking successful")
                vehicle.status = 'in_use'  # change vehicle status
                vehicle.save()
        except Exception as e:
            logging.error(str(e))
            return Response(data={"error": {"error": type(e).__name__, "message": str(e)}})
        return Response(data={"data": booking_serializer.data}, status=status.HTTP_201_CREATED)


class VehicleReturnView(APIView):
    def get(self, request):
        try:
            booking_id = request.GET.get("booking_id")
            booking = VehicleBooking.objects.get(booking_id=booking_id)

            vehicle = Vehicle.objects.get(vehicle_id=booking.vehicle.vehicle_id)
            vehicle.status = "available"
            vehicle.save()
        except Exception as e:
            logging.error(str(e))
            return Response(data={"error": {"error": type(e).__name__, "message": str(e)}})
        return Response(data={"data": "Vehicle Returned Successfully"}, status=status.HTTP_200_OK)