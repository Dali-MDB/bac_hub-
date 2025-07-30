from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
import pandas as pd
from django.conf import settings
from main.models import Field,Subject
from .serializers import SubjectSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser


def matching_fields(row):
    """
    Helper function to match fields with their coefficients from a CSV row
    """
    counter = {}
    for field in Field:
        coef = row[field]    #get the coef of the current field
        if pd.isna(coef):
            continue   #skip in nan
        if coef in counter:
            counter[coef].append(field)
        else:
            counter[coef] = [field]
    return counter


def create_subjects(name:str,counter:dict):
    """
    Helper function to create subjects based on field coefficients
    """
    for coef,fields in counter.items():
        try:
            subject = Subject.objects.create(
                name = name+':'+ str(coef),
                field = fields,
                coefficient = coef
            )
            subject.save()
        except:
            print("error occured with "+name)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def init_subjects(request):
    """
    Endpoint: GET /initialize_subjects/
    Description: Initialize subjects and their coefficients from CSV file
    Authentication: Not required
    Response: {"details": "success"}
    Notes: This endpoint should only be run once to populate the database
    """
    file_path = settings.BASE_DIR/'main/bac_fields_subjects.csv'
   
    df = pd.read_csv(file_path)
    for index,row in df.iterrows():
        #get matching coefs for eaxh field
        counter = matching_fields(row)
        #create the subjects
        create_subjects(row['المادة'],counter)
        
    
    return Response(
        {'details':'success'}
    )


@api_view(['GET'])
def get_all_subjects(request):
    """
    Endpoint: GET /subjects/
    Description: Get all available subjects organized by field
    Authentication: Not required
    Response: Dictionary with subjects grouped by field
    Example: {"علوم تجريبية": [...], "رياضيات": [...], ...}
    """
    subjects = Subject.objects.all()
    subjects_by_field = {
        Field.EXPERIMENTAL_SCIENCES : [],
        Field.MATHEMATICS : [],
        Field.TECHNICAL_MATHEMATICS : [],
        Field.MANAGEMENT_ECONOMICS : [],
        Field.LITERATURE_PHILOSOPHY : [],
        Field.FOREIGN_LANGUAGES : []
    }
    for subject in subjects:
        serializer = SubjectSerializer(subject)
        subjects_by_field[subject.field].append(serializer.data)
    return Response(subjects_by_field,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_subject(request,sub_id:int):
    """
    Endpoint: POST /subjects/{sub_id}/
    Description: Add a new subject (currently not fully implemented)
    Authentication: Not required
    Parameters: sub_id (integer) - Subject ID
    """
    subject = get_object_or_404(Subject,id=sub_id)
    serializer = SubjectSerializer(subject,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_subject(request,sub_id:int):
    """
    Endpoint: GET /subjects/{sub_id}/
    Description: Get a specific subject by ID
    Authentication: Not required
    Parameters: sub_id (integer) - Subject ID
    Response: Subject object with id, name, field, coefficient
    """
    subject = get_object_or_404(Subject,id=sub_id)
    serializer = SubjectSerializer(subject)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_subject(request,sub_id:int):
    """
    Endpoint: PUT /subjects/{sub_id}/
    Description: Update a specific subject
    Authentication: Not required
    Parameters: sub_id (integer) - Subject ID
    Request Body: {"name": "string", "coefficient": "integer"}
    Response: Updated subject object
    """
    subject = get_object_or_404(Subject,id=sub_id)
    serializer = SubjectSerializer(subject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_subject(request,sub_id:int):
    """
    Endpoint: DELETE /subjects/{sub_id}/
    Description: Delete a specific subject
    Authentication: Not required
    Parameters: sub_id (integer) - Subject ID
    Response: 204 No Content
    """
    subject = get_object_or_404(Subject,id=sub_id)
    subject.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_subjects_by_field(request):
    """
    Endpoint: GET /subjects/field/?field={field_name}
    Description: Get subjects related to a specific field
    Authentication: Not required
    Query Parameters: field (string) - Field name
    Response: Array of subjects for the specified field
    Example: [{"id": 1, "name": "string", "field": ["علوم تجريبية"], "coefficient": 3}]
    """
    field = request.GET.get('field',None)
    if not field:
        raise ValidationError(detail='this field is notregistered within our system',code=400)
    else:
        subjects = Subject.objects.filter(field__contains=field)
    serializer = SubjectSerializer(subjects,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)