from rest_framework import generics
from .models import User, Dealership
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, ResetPasswordSerializer, DealershipSerializer
from rest_framework.response import Response
from user.utils import get_user_from_token
from rest_framework.decorators import authentication_classes

# from rest_framework.permissions import IsAdminUser


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.validated_data
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(serializer.data)
            return Response({'message': 'Password reset successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom token refresh view using Simple JWT.
    Handles refreshing access tokens via refresh tokens.
    """
    permission_classes = [permissions.AllowAny]  # Set permissions as needed

    def post(self, request, *args, **kwargs):
        # Call the parent class's post method to handle token refresh
        return super().post(request, *args, **kwargs)


@authentication_classes([])
class CreateDealershipView(APIView):

    def post(self, request):
        print('ali')
        try:
            auth_header = request.headers.get('Authorization')
            user = get_user_from_token(auth_header)
        except:
            return Response({'error': 'Invalid token'})
        serializer = DealershipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

