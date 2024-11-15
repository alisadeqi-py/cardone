import jwt
from datetime import datetime
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status
from functools import wraps


def get_user_from_token(auth_header):
    # Extract the token from the request headers

    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthenticationFailed('Authorization token not provided or invalid format')

    # Get the token
    token = auth_header.split(' ')[1]

    try:
        # Decode the JWT manually
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        # Check if the token is expired
        exp_timestamp = payload.get('exp')
        if exp_timestamp:
            exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
            if exp_datetime < datetime.utcnow():
                raise AuthenticationFailed('Token has expired')

        # Retrieve the user from the payload
        user_id = payload.get('user_id')
        if not user_id:
            raise AuthenticationFailed('Invalid token: user ID not found')

        # Fetch the user from the database
        user = User.objects.filter(userId=user_id, isDeleted=False).first()
        if not user:
            raise AuthenticationFailed('User not found or deleted')

        return user

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.DecodeError:
        raise AuthenticationFailed('Error decoding token')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')


def jwt_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Retrieve the authorization header from the request
        auth_header = request.headers.get('Authorization', None)

        if auth_header is None or not auth_header.startswith('Bearer '):
            return Response({"detail": "Authentication credentials were not provided."},
                            status = status.HTTP_401_UNAUTHORIZED)

        # Extract the JWT token from the Authorization header
        token = auth_header.split(" ")[1]

        try:
            # Validate the token using Simple JWT
            access_token = AccessToken(token)
            # If the token is valid, continue with the view
            return view_func(request, *args, **kwargs)

        except (InvalidToken, TokenError):
            return Response({"detail": "Invalid or expired token."}, status = status.HTTP_401_UNAUTHORIZED)

    return _wrapped_view
