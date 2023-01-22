from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from .serializers import StationSerializer


# Create your views here.
class StationCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        user = request.user
        data["owner"] = user.id

        serializer = StationSerializer(data=data)
        if serializer.is_valid():
            station = serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)