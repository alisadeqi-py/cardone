from rest_framework_mongoengine.serializers import DocumentSerializer
from bson import ObjectId
from rest_framework import serializers
from .models import Car, Dealership


class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError("Invalid ObjectId")


class CarSerializer(DocumentSerializer):
   # dealerId = ObjectIdField()  # Handle ObjectId for the owner field

    class Meta:
        model = Car
        fields = '__all__'