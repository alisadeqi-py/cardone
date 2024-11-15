from rest_framework import generics
from .models import Customer
from rest_framework import status
from .serializers import CustomerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from user.utils import get_user_from_token
from user.models import Dealership
from rest_framework.decorators import authentication_classes


# Create your views here.
@authentication_classes([])
class CustomerCreateAPIView(APIView):

    def post(self, request):
        # Initialize the serializer with request data
        serializer = CustomerSerializer(data = request.data)

        # Validate the data
        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        # Save the validated data to create a new customer instance
        customer_instance = serializer.save()

        # Serialize the created instance and return as a response
        final_serializer = CustomerSerializer(customer_instance)
        return Response(final_serializer.data, status = status.HTTP_201_CREATED)

    def get(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            user = get_user_from_token(auth_header)
        except:
            return Response({'error': 'Invalid token'})
        print('user', user)
        # Retrieve all customer instances
        dealer_id = Dealership.objects.get(owner = user).id
        print('dealerId', dealer_id)
        customers = Customer.objects.filter(dealerId = dealer_id).get()
        serializer = CustomerSerializer(customers)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 671b6256cecdfa9224f6d9b2
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'CustomerId'  # Or '_id' if using Mongo's default ID field
