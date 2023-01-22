from django.urls import path
from . import views

urlpatterns = [path('create/', views.StationCreateView.as_view(), name="create_station")]
