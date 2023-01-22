from django.urls import path
from . import views

urlpatterns = [
    path('vehicles/', views.StationView.as_view(), name="list_vehicles"),
    path('create/', views.StationView.as_view(), name="create_station"),
]