from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from authentication.serializers import ProfileSerializer
from main.models import Profile
from django.shortcuts import get_object_or_404






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_my_profile(request):
    """
    Endpoint: GET /users/profile/me/view/
    Description: Get current user's profile
    Authentication: Required
    Response: Profile object with user details, field, city, school_name, xp
    """

    user = request.user
    serializer = ProfileSerializer(user.profile)
    return Response(serializer.data,status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_my_profile(request):
    """
    Endpoint: PUT /users/profile/me/update/
    Description: Update current user's profile
    Authentication: Required
    Request Body: {"field": "string", "city": "string", "school_name": "string"}
    Response: Updated profile object
    """
    user = request.user
    serializer = ProfileSerializer(user.profile,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['GET'])
def get_all_profiles(request):
    """
    Endpoint: GET /users/profile/all/
    Description: Get all user profiles
    Authentication: Not required
    Response: Array of profile objects
    """
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)



@api_view(['GET'])
def get_profile(request,profile_id:int):
    """
    Endpoint: GET /users/profile/{profile_id}/
    Description: Get specific user profile by ID
    Authentication: Not required
    Parameters: profile_id (integer) - Profile ID
    Response: Profile object
    """
    profile = get_object_or_404(Profile,id=profile_id)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def get_current_user(request):
    is_authenticated = request.user.is_authenticated
    id = request.user.id if is_authenticated else None
    return Response({
        "is_authenticated" : is_authenticated,
        "id" : id,
    })


