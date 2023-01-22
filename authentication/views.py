from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
import logging
import requests
import os
from django.core.cache import cache

TWO_FACTOR_API_KEY = os.getenv("TWO_FACTOR_API_KEY")


class Index(APIView):
    """
    Home page
    """
    def get(self, request):
        content = {'message': 'Welcome To Vehicle Rental Store'}
        return Response(content)


class SendPhoneOtpView(APIView):
    def send_phone_otp(self, phone_number: str):
        """Send OTP to phone using 2-factor OTP API"""
        url = f"http://2factor.in/API/V1/{TWO_FACTOR_API_KEY}/SMS/{phone_number}/AUTOGEN"

        payload = ""
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("GET", url, data=payload, headers=headers)
        data = response.json()
        session_id = data.get("Details")
        if data.get("Status") == "Success":
            logging.info("OTP sent successfully")
            return session_id
        logging.error("Failed to send OTP")
        return None

    def post(self, request, *args, **kwargs):
        data = request.data

        phone = data["phone"]
        # Check for any existing user
        user = User.objects.filter(phone=phone)
        if user:
            return Response(
                data="User already exists, Please login using Phone & Password.", status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(data=request.data)  # Serialize and validate the data
        if serializer.is_valid():
            session_id = self.send_phone_otp(phone)
            if not session_id:
                return Response(
                    data={"error": "Unable to send OTP, Please enter valid phone number"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # caching the user data and OTP data for verification, OTP valid for 10 Minutes
            cache.add(key=phone, value={"session_id": session_id, "user_data": data}, timeout=600)
            return Response(data={"message": "OTP is sent to your phone number"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneOtpView(APIView):
    def verify_otp(self, session_id, otp):

        url = f"https://2factor.in/API/V1/{TWO_FACTOR_API_KEY}/SMS/VERIFY/{session_id}/{otp}"
        payload = ""
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("GET", url, data=payload, headers=headers)
        data = response.json()
        if data.get("Status") == "Success" and data.get("Details") == "OTP Matched":
            logging.info("Phone number verified successfully")
            return True
        return False

    def post(self, request, *args, **kwargs):
        data = request.data
        phone = data.get("phone")
        saved_data = cache.get(phone)
        if not saved_data:
            return Response(
                data={"message": "OTP expired 🙂!!!, Please try again."}, status=status.HTTP_408_REQUEST_TIMEOUT
            )

        # OTP Verification
        is_otp_valid = self.verify_otp(session_id=saved_data["session_id"], otp=data.get("otp"))
        if is_otp_valid:
            user_data = saved_data["user_data"]
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                user = serializer.save()  # If data is valid, user will be created successfully
                cache.delete(key=phone)  # Remove users data from cache
                return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"error": "OTP Invalid !!!, please enter correct OTP"}, status=status.HTTP_400_BAD_REQUEST)
