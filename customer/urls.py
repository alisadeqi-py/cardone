from django.urls import path
from .views import CustomerCreateAPIView, CustomerDetailView

urlpatterns = [
    path('manage',  CustomerCreateAPIView.as_view(), name='customer_list_create'),
    #path('<str:CustomerId>/', CustomerDetailView.as_view(), name='customer_detail')
]