import boto3
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .models import Car
from .serializers import CarSerializer
from rest_framework.decorators import authentication_classes
from user.utils import get_user_from_token
from user.models import Dealership


@authentication_classes([])  # No authentication required
class CarListAPIView(APIView):


    def get(self, request):

        try:
            auth_header = request.headers.get('Authorization')
            user = get_user_from_token(auth_header)
        except:
            return Response({'error': 'Invalid token'})


        try:
            dealerId = Dealership.objects.filter(owner = user).get()
        except:
            return Response({'message': 'this user does not have any dealership'})

        # Retrieve all Car objects
        cars = Car.objects.filter(isDeleted = False, dealerId = dealerId)  # Filter out soft-deleted cars
        serializer = CarSerializer(cars, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)


@authentication_classes([])
class CarDetailAPIView(APIView):

    def get(self, request, pk):

        try:
            auth_header = request.headers.get('Authorization')
            user = get_user_from_token(auth_header)
        except:
            return Response({'error': 'Invalid token'})

        try:
            dealerId = Dealership.objects.filter(owner = user).get()
        except:
            return Response({'message': 'this user does not have any dealership'})

        try:
            cars = Car.objects.filter(isDeleted = False, dealerId = dealerId, carId = pk)
            serializer = CarSerializer(cars, many = True)
        except:
            return Response({'message': 'car does not exists'})

        return Response(serializer.data, status = status.HTTP_200_OK)


class CarCreateAPIView(APIView):
    def post(self, request):

        try:
            auth_header = request.headers.get('Authorization')
            user = get_user_from_token(auth_header)
        except:
            return Response({'error': 'Invalid token'})


        # Serialize the request data
        car_data = request.data.copy()
        car_data.pop('photos', None)  # Remove photos from the data
        print(car_data)
        serializer = CarSerializer(data = car_data)
        if not serializer.is_valid():
             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        car_instance = serializer.save()
        # Handle file uploads to S3 if files are included
        photos = request.FILES.getlist('photos')
        print('photos:', photos)
        uploaded_photo_urls = []
        session = boto3.session.Session()

        # Initialize AWS S3 session
        s3_client = session.client(
            's3',
            endpoint_url = settings.AWS_END_POINT,
            aws_access_key_id = settings.AWS_ACCESS_KEY,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
            #AWS_S3_REGION_NAME = "us-east-1"
        )
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        print('dealerId:', car_instance.dealerId)
        # Upload each photo to S3 and generate a public URL
        for photo in photos:
            file_path = f"cars/{car_instance.id}/{photo.name}" # Use dealerId from request data
            print(file_path)
            try:
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                s3_client.put_object(Key = file_path, Body = photo, ContentType = photo.content_type, Bucket=bucket_name,)

                # Generate the public URL for the uploaded photo
                photo_url = f"https://{bucket_name}.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_path}"
                uploaded_photo_urls.append(photo_url)
            except Exception as e:
                return Response({'error': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        # At this point, all photos have been uploaded successfully
        # Now save the Car instance with the uploaded photo URLs
        car_instance = serializer.save(photos = uploaded_photo_urls)  # Save with photo URLs

        # Serialize and return the updated Car instance
        final_serializer = CarSerializer(car_instance)
        return Response(final_serializer.data, status = status.HTTP_201_CREATED)



