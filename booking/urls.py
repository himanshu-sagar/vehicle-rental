from django.urls import path
from . import views

urlpatterns = [
    path('book_vehicle/', views.VehicleBookingView.as_view(), name="book_vehicle"),
    path('return_vehicle/', views.VehicleReturnView.as_view(), name="return_vehicle")
]
