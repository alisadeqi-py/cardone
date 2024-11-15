from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Dealership
from bson import ObjectId
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import User, Dealership
import re


class UserSerializer(DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError("Invalid ObjectId")


class DealershipSerializer(DocumentSerializer):
    owner = ObjectIdField()  # Handle ObjectId for the owner field

    class Meta:
        model = Dealership
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    firstName = serializers.CharField(max_length=50, required=False)
    lastName = serializers.CharField(max_length=50, required=False)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    gender = serializers.ChoiceField(choices=['Male', 'Female', 'Other'])
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_phone(self, value):
        # Simple regex to validate phone number format
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Invalid phone number format")
        return value

    def validate_email(self, value):
        # Check if the email already exists
        if User.objects(email=value).first():
            raise serializers.ValidationError("Email is already in use")
        return value

    def validate_Username(self, value):
        # Check if the Username already exists
        if User.objects(Username=value).first():
            raise serializers.ValidationError("Username is already taken")
        return value

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        user_instance = User(**validated_data)
        user_instance .save()
        return User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Retrieve the User by email
        email = data.get('email')
        password = data.get('password')

        try:
            User_instance = User.objects.get(email=email)
        except :
            raise serializers.ValidationError("Invalid email or password")

        # Check if the password is correct
        if not check_password(password, User_instance.password):
            raise serializers.ValidationError("Invalid email or password")

        # Generate and return tokens
        refresh = RefreshToken.for_user(User_instance)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    current_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(min_length = 12)

    def validate(self, data):
        email = data.get('email')
        current_password = data.get('current_password')

        # Check if the User exists
        try:
            User = User.objects.get(email = email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        # Verify the current password
        if not check_password(current_password, User.password):
            raise serializers.ValidationError("Current password is incorrect")

        return data

    def save(self, validated_data):
        email = validated_data['email']
        new_password = validated_data['new_password']

        User = User.objects.get(email = email)
        User.password = make_password(new_password)  # Hash the new password
        User.save()
        return User


class DealershipSerializer(DocumentSerializer):
    class Meta:
        model = Dealership
        fields = [
            'address', 'owner', 'salesVolume', 'domain',
            'staffs', 'phone1', 'phone2', 'phone3', 'city', 'state',
            'isLegal', 'customers'
        ]
        read_only_fields = ['dateCreated', 'dateUpdated', 'isDeleted']
