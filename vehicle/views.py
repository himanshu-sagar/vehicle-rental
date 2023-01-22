from rest_framework.views import APIView, Response, status
from .qr_code import QrCode
from rest_framework.permissions import IsAuthenticated
from .serializers import VehicleSerializer
import logging


# Create your views here.
class VehicleCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data

        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            vehicle = serializer.save()
            # Generating and saving QR Code, Print it and paste it on the vehicle
            qrcode = QrCode(serializer.data["vehicle_id"])
            path = qrcode.generate_qr_code()
            return Response(data={"vehicle": serializer.data, "qr_code_path": path}, status=status.HTTP_201_CREATED)
        return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Use this if want to generate QR code seperately using vehicle_id
class QRCodeGenerateView(APIView):
    def get(self, request):
        try:
            qrcode = QrCode(request.GET.get("vehicle_id"))
            res = qrcode.generate_qr_code()
        except Exception as e:
            logging.error(str(e))
            return Response(data={"error": {"error": type(e).__name__, "message": str(e)}})
        return Response(data={"data": {"qr_path": res}}, status=status.HTTP_200_OK)
