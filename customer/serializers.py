from rest_framework import serializers
from .models import Customer
from django.utils import timezone


class CustomerSerializer(serializers.Serializer):
    firstName = serializers.CharField(max_length=100, required=True)
    lastName = serializers.CharField(max_length=50, required=True)
    phone = serializers.CharField(max_length=15, required=False)
    gender = serializers.ChoiceField(choices=['Male', 'Female', 'Other'], required=True)
    dealerId = serializers.CharField(required=True)

    def create(self, validated_data):
        # Create a new customer instance
        customer_instance = Customer(
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            phone=validated_data.get('phone', ''),
            gender=validated_data['gender'],
            dealerId=validated_data['dealerId'],
            dateCreated=timezone.now(),
            dateUpdated=timezone.now()
        )
        customer_instance.save()
        return customer_instance

    def to_representation(self, instance):
        # Customize the representation of the Customer instance
        return {
            "firstName": instance.firstName,
            "lastName": instance.lastName,
            "phone": instance.phone,
            "gender": instance.gender,
            "dealerId": str(instance.dealerId),  # Assuming dealerId is a reference, you might want to return a specific field from it
            "dateCreated": instance.dateCreated,
            "dateUpdated": instance.dateUpdated,
            "CustomerId": str(instance.CustomerId)  # Including the CustomerId for identification
        }