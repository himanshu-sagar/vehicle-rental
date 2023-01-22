from django.urls import path
from . import views

urlpatterns = [path('create/', views.VehicleCreateView.as_view(), name="add_vehicle")]
