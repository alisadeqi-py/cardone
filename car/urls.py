from django.urls import path
from .views import CarListAPIView, CarDetailAPIView, CarCreateAPIView

urlpatterns = [
    path('list', CarListAPIView.as_view(), name='car_list_create'),
    path('create', CarCreateAPIView.as_view(), name='car_detail'),
    path('<str:CarId>/', CarDetailAPIView.as_view(), name='car_detail'),

]