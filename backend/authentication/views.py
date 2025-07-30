from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer,ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from main.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def home(request):
    """
    Simple test endpoint to verify API is working
    """
    return Response({'message':'hello world'})


@api_view(['POST'])
def register(request):
    """
    Endpoint: POST /authentication/register/
    Description: Register a new user account
    Authentication: Not required
    Request Body: {"user": {"username": "string", "email": "string", "password": "string", "first_name":"string", "last_name":"string"}, "field": "string", "city": "string", "school_name": "string"}
    Response: {"details": {...}, "success": "string", "refresh": "string", "access": "string"}
    """
    profile_ser = ProfileSerializer(data=request.data)
    if profile_ser.is_valid():
        profile = profile_ser.save()
        #we generate refresh and access tokens
        refresh = RefreshToken.for_user(profile.user)
        context = {
            'details' : profile_ser.data,
            'success' : 'user created successfully',
            'refresh' : str(refresh),
            'access' :  str(refresh.access_token)
        }
        return  Response(context, status=status.HTTP_201_CREATED)
    return Response(profile_ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """
    Endpoint: POST /authentication/login/
    Description: Login user and get JWT tokens
    Authentication: Not required
    Request Body: {"email": "string", "password": "string"}
    Response: {"refresh": "string", "access": "string"}
    """
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    #we query for the user with the specified email
    user = get_object_or_404(User,email=email)
    #we authenticated te user
    username = user.username
    user = authenticate(username=username,password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }
        return Response(tokens, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Endpoint: POST /authentication/change_password/
    Description: Change user password
    Authentication: Required
    Request Body: {"old_password": "string", "new_password": "string", "new_password_confirm": "string"}
    Response: {"message": "Password changed successfully"s}
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    new_password_confirm = request.data.get('new_password_confirm')
    #we validate existence and matching
    if not old_password or not new_password or not new_password_confirm:
        return Response({'error': 'all fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    if new_password != new_password_confirm:
        return Response({'error': 'passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    
    #check if the old password is correct
    if not user.check_password(old_password):
        return Response({'error': 'old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    #we set the new password
    user.set_password(new_password)
    user.save()
    #we return a success message
    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    Test endpoint that requires authentication
    """
    return Response({"success":"you are allowed to view this page"})


@api_view(['POST'])
def get_refresh(request):
    """
    Endpoint: POST /authentication/get_refresh/
    Description: Get new access token using refresh token
    Authentication: Not required
    Request Body: {"refresh": "string"}
    Response: {"access": "string"} or {"error": "string"}
    """
    try:
        access = str(RefreshToken(request.data['refresh']).access_token)
        return Response({'access':access})
    except:
        return Response({'error':'the given token has been blacklisted'})