from django.urls import path
from . import views

urlpatterns = [
    # path('', views.Index.as_view(), name='home'),
    #path('signup/', views.SignupAPIView.as_view(), name="signup"),
    path('send_otp/', views.SendPhoneOtpView.as_view(), name="send_otp"),
    path('verify_otp/', views.VerifyPhoneOtpView.as_view(), name="verify_otp")
]
