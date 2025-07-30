from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from main.models import Resource,Question,Reply,ImageQuestion,ImageReply
from main.models import ResourceType
from .serializers import ResourceSerializer,QuestionSerializer,ReplySerializer,ImageQuestionSerializer,ImageReplySerializer
from django.shortcuts import get_object_or_404
import json
from main.models import Field
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

#get all resources
@api_view(['GET'])
def get_all_resources(request):
    """
    Endpoint: GET /resources/all/
    Description: Get all resources organized by type
    Authentication: Not required
    Response: Dictionary with resources grouped by type (EXAM, SUMMARY, NOTES, TEXT_BOOKS, VIDEO)
    """
    resources = Resource.objects.all().order_by('-created_at')
    #split them by type
    resources_by_type = {
        ResourceType.EXAM : [],
        ResourceType.SUMMARY : [],
        ResourceType.NOTES : [],
        ResourceType.TEXT_BOOKS : [],
        ResourceType.VIDEO : []
    }
    for resource in resources:
        serializer = ResourceSerializer(resource)
        resources_by_type[resource.type].append(serializer.data)

    return Response(resources_by_type,status=status.HTTP_200_OK)


#get a resource by id
@api_view(['GET'])
def get_resource(request,resource_id:int):
    """
    Endpoint: GET /resources/{resource_id}/
    Description: Get a specific resource by ID
    Authentication: Not required
    Parameters: resource_id (integer) - Resource ID
    Response: Resource object with all details
    """
    resource = get_object_or_404(Resource,id=resource_id)
    serializer = ResourceSerializer(resource)
    return Response(serializer.data,status=status.HTTP_200_OK)


#get all resources by author
@api_view(['GET'])
def get_resources_by_author(request,author_id:int):
    """
    Endpoint: GET /resources/author/{author_id}/
    Description: Get all resources by a specific author
    Authentication: Not required
    Parameters: author_id (integer) - User ID
    Response: Array of resource objects
    """
    resources = Resource.objects.filter(author=author_id)
    serializer = ResourceSerializer(resources,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


#get all resources by subject
@api_view(['GET'])
def get_resources_by_subject(request,subject_id:int):
    """
    Endpoint: GET /resources/subject/{subject_id}/
    Description: Get all resources for a specific subject
    Authentication: Not required
    Parameters: subject_id (integer) - Subject ID
    Response: Array of resource objects
    """
    resources = Resource.objects.filter(subject=subject_id)
    serializer = ResourceSerializer(resources,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_resource(request):
    """
    Endpoint: POST /resources/add/
    Description: Add a new resource
    Authentication: Required
    Request Body: {"name": "string", "description": "string", "subject": 1, "type": "string", "labels": "string", "link": "string", "additional_link": "string"}
    Response: Created resource object
    """
    data = request.data
    data['author'] = request.user.id
    resource_ser = ResourceSerializer(data=data)
    if resource_ser.is_valid():
        resource_ser.save() 
        return Response(resource_ser.data,status=status.HTTP_200_OK)
    else:
        return Response(resource_ser.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_resource(request,resource_id:int):
    """
    Endpoint: PUT /resources/update/{resource_id}/
    Description: Update a resource (only by author)
    Authentication: Required
    Parameters: resource_id (integer) - Resource ID
    Request Body: Partial resource object
    Response: Updated resource object
    """
    resource = get_object_or_404(Resource,id=resource_id)
    if resource.author != request.user:
        return Response({'error': 'You are not the author of this resource'},status=status.HTTP_403_FORBIDDEN)
    serializer = ResourceSerializer(resource,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_resource(request,resource_id:int):
    """
    Endpoint: DELETE /resources/delete/{resource_id}/
    Description: Delete a resource (only by author or staff)
    Authentication: Required
    Parameters: resource_id (integer) - Resource ID
    Response: 204 No Content
    """
    resource = get_object_or_404(Resource,id=resource_id)
    if resource.author != request.user and not request.user.is_staff:
        return Response({'error': 'You are not the author of this resource'},status=status.HTTP_403_FORBIDDEN)
    resource.delete()
    return Response({'detail': 'Resource deleted successfully'},status=status.HTTP_204_NO_CONTENT)

#ensure throttling for this end point
from .throttling import ResourceReportThrottle
from rest_framework.decorators import throttle_classes


#@throttle_classes([ResourceReportThrottle])
@api_view(['POST'])
def report_resource(request,resource_id:int):
    """
    Endpoint: POST /resources/report/{resource_id}/
    Description: Report a resource for inappropriate content
    Authentication: Not required
    Parameters: resource_id (integer) - Resource ID
    Response: {"detail": "Resource reported successfully"}
    """
    #apply the throttle (since the end point is not authenticated we need to call it manually)
    throttle = ResourceReportThrottle()
    if not throttle.allow_request(request, None):
        return Response({
            'error': 'Rate limit exceeded',
            'detail': 'You can only report this resource once per day'
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    resource = get_object_or_404(Resource,id=resource_id)
    resource.add_report()
    resource.save()
    return Response({'detail': 'Resource reported successfully'},status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_question(request):
    """
    Endpoint: POST /resources/question/add/
    Description: Add a new question
    Authentication: Required
    Request Body: {"subject": 1, "content": "string"}
    Response: Created question object
    """
    data = request.data
    data['author'] = request.user.id
    question_ser = QuestionSerializer(data=data)
    if question_ser.is_valid():
        question_ser.save()
        return Response(question_ser.data,status=status.HTTP_200_OK)
    else:
        return Response(question_ser.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_question(request,question_id:int):
    """
    Endpoint: GET /resources/question/{question_id}/
    Description: Get a specific question by ID
    Authentication: Not required
    Parameters: question_id (integer) - Question ID
    Response: Question object with all details
    """
    question = get_object_or_404(Question,id=question_id)
    serializer = QuestionSerializer(question)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_question(request,question_id:int):
    """
    Endpoint: PUT /resources/question/update/{question_id}/
    Description: Update a question (only by author)
    Authentication: Required
    Parameters: question_id (integer) - Question ID
    Request Body: Partial question object
    Response: Updated question object
    """
    question = get_object_or_404(Question,id=question_id)
    if question.author != request.user:
        return Response({'error': 'You are not the author of this question'},status=status.HTTP_403_FORBIDDEN)
    serializer = QuestionSerializer(question,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_question(request,question_id:int):
    """
    Endpoint: DELETE /resources/question/delete/{question_id}/
    Description: Delete a question (only by author or staff)
    Authentication: Required
    Parameters: question_id (integer) - Question ID
    Response: 204 No Content
    """
    question = get_object_or_404(Question,id=question_id)
    if question.author != request.user and not request.user.is_staff:
        return Response({'error': 'You are not the author of this question'},status=status.HTTP_403_FORBIDDEN)
    question.delete()
    return Response({'detail': 'Question deleted successfully'},status=status.HTTP_204_NO_CONTENT)



from .throttling import QuestionReportThrottle
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_question(request,question_id:int):
    """
    Endpoint: POST /resources/question/report/{question_id}/
    Description: Report a question for inappropriate content
    Authentication: Required
    Parameters: question_id (integer) - Question ID
    Response: {"detail": "Question reported successfully"}
    """
    throttle = QuestionReportThrottle()
    if not throttle.allow_request(request,None):
        return Response({
            'error': 'Rate limit exceeded',
            'detail': 'You can only report this question once per 2 h'
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    question = get_object_or_404(Question,id=question_id)
    question.add_report()
    #question.save()
    return Response({'detail': 'Question reported successfully'},status=status.HTTP_200_OK)


#get all questions by subject
@api_view(['GET'])
def get_question_by_subject(request,subject_id:int):
    """
    Endpoint: GET /resources/question/subject/{subject_id}/
    Description: Get all questions for a specific subject
    Authentication: Not required
    Parameters: subject_id (integer) - Subject ID
    Response: Array of question objects
    """
    questions = Question.objects.filter(subject=subject_id)
    serializer = QuestionSerializer(questions,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


#get all questions by author
@api_view(['GET'])
def get_questions_by_author(request,author_id:int):
    """
    Endpoint: GET /resources/question/author/{author_id}/
    Description: Get all questions by a specific author
    Authentication: Not required
    Parameters: author_id (integer) - User ID
    Response: Array of question objects
    """
    questions = Question.objects.filter(author=author_id)
    serializer = QuestionSerializer(questions,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_reply(request):
    """
    Endpoint: POST /resources/reply/add/
    Description: Add a new reply to a question
    Authentication: Required
    Request Body: {"question": 1, "parent": 1 (optional), "content": "string"}
    Response: Created reply object with nested children
    """
    data = request.data
    data['author'] = request.user.id
    reply_ser = ReplySerializer(data=data)
    if reply_ser.is_valid():
        reply_ser.save()
        return Response(reply_ser.data,status=status.HTTP_200_OK)
    else:
        return Response(reply_ser.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_reply(request,reply_id:int):
    """
    Endpoint: GET /resources/reply/{reply_id}/
    Description: Get a specific reply by ID
    Authentication: Not required
    Parameters: reply_id (integer) - Reply ID
    Response: Reply object with nested children
    """
    reply = get_object_or_404(Reply,id=reply_id)
    serializer = ReplySerializer(reply)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_reply(request,reply_id:int):
    """
    Endpoint: PUT /resources/reply/update/{reply_id}/
    Description: Update a reply (only by author)
    Authentication: Required
    Parameters: reply_id (integer) - Reply ID
    Request Body: Partial reply object
    Response: Updated reply object
    """
    reply = get_object_or_404(Reply,id=reply_id)
    if reply.author != request.user:
        return Response({'error': 'You are not the author of this reply'},status=status.HTTP_403_FORBIDDEN)
    serializer = ReplySerializer(reply,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)  
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reply(request,reply_id:int):
    """
    Endpoint: DELETE /resources/reply/delete/{reply_id}/
    Description: Delete a reply (only by author or staff)
    Authentication: Required
    Parameters: reply_id (integer) - Reply ID
    Response: 204 No Content
    """
    reply = get_object_or_404(Reply,id=reply_id)
    if reply.author != request.user and not request.user.is_staff:
        return Response({'error': 'You are not the author of this reply'},status=status.HTTP_403_FORBIDDEN)
    reply.delete()
    return Response({'detail': 'Reply deleted successfully'},status=status.HTTP_204_NO_CONTENT)


from .throttling import ReplyReportThrottle
@api_view(['POST'])
def report_reply(request,reply_id:int):
    """
    Endpoint: POST /resources/reply/report/{reply_id}/
    Description: Report a reply for inappropriate content
    Authentication: Not required
    Parameters: reply_id (integer) - Reply ID
    Response: {"detail": "Reply reported successfully"}
    """
    throttle = ReplyReportThrottle()
    if not throttle.allow_request(request,None):
        return Response({
            'error': 'Rate limit exceeded',
            'detail': 'You can only report this reply once per 2 h'
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    reply = get_object_or_404(Reply,id=reply_id)
    reply.add_report()
    return Response({'detail': 'Reply reported successfully'},status=status.HTTP_200_OK)


@api_view(['GET'])
def get_replies_by_question(request,question_id:int):
    """
    Endpoint: GET /resources/reply/question/{question_id}/
    Description: Get all replies for a specific question
    Authentication: Not required
    Parameters: question_id (integer) - Question ID
    Response: Array of reply objects
    """
    replies = Reply.objects.filter(question=question_id)
    replies_ser = ReplySerializer(replies,many=True)
    return Response(replies_ser.data,status=status.HTTP_200_OK)


#handling images
def create_images(rel,rel_id,images,SERIALIZER):
    errors = False
    for image in images:
        image_ser = SERIALIZER(data={'img':image,f'{rel}':rel_id})
        if image_ser.is_valid():
            image_ser.save()
        else:
            print(image_ser.errors)
            errors = True
    return errors


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_images_to_qst(request,qst_id):
    """
    Endpoint: POST /resources/question/images/{qst_id}/upload/
    Description: Upload images to a question (only by author or staff)
    Authentication: Required
    Parameters: qst_id (integer) - Question ID
    Request Body: FormData with 'images' field containing multiple image files
    Response: {"details": "the images have been added successfully"}
    """
    question = get_object_or_404(Question,id=qst_id)
    if question.author != request.user and not request.user.is_staff:
        return Response({'error': 'You are not the author of this reply'},status=status.HTTP_403_FORBIDDEN)
    images = request.FILES.getlist('images')

    if create_images('question',qst_id,images,ImageQuestionSerializer):
        return Response({'error': 'There were some issues adding some images'},status=status.HTTP_400_BAD_REQUEST)
    return Response({'details':'the images have been added successfully'},status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_images_to_reply(request,reply_id):
    """
    Endpoint: POST /resources/reply/images/{reply_id}/upload/
    Description: Upload images to a reply (only by author or staff)
    Authentication: Required
    Parameters: reply_id (integer) - Reply ID
    Request Body: FormData with 'images' field containing multiple image files
    Response: {"details": "the images have been added successfully"}
    """
    reply = get_object_or_404(Reply,id=reply_id)
    if reply.author != request.user and not request.user.is_staff:
        return Response({'error': 'You are not the author of this reply'},status=status.HTTP_403_FORBIDDEN)
    images = request.FILES.getlist('images')

    if create_images('reply',reply_id,images,ImageReplySerializer):
        return Response({'error': 'There were some issues adding some images'},status=status.HTTP_400_BAD_REQUEST)
    return Response({'details':'the images have been added successfully'},status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_qst_images(request,qst_id):
    """
    Endpoint: GET /resources/question/images/{qst_id}/view/
    Description: Get all images for a specific question
    Authentication: Not required
    Parameters: qst_id (integer) - Question ID
    Response: Array of image objects with URLs
    """
    images = ImageQuestion.objects.filter(question=qst_id)
    images_ser = ImageQuestionSerializer(images,many=True)
    return Response(images_ser.data)


@api_view(['GET'])
def get_reply_images(request,reply_id):
    """
    Endpoint: GET /resources/reply/images/{reply_id}/view/
    Description: Get all images for a specific reply
    Authentication: Not required
    Parameters: reply_id (integer) - Reply ID
    Response: Array of image objects with URLs
    """
    images = ImageReply.objects.filter(reply=reply_id)
    images_ser = ImageReplySerializer(images,many=True)
    return Response(images_ser.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_qst_images(request,qst_id):
    """
    Endpoint: DELETE /resources/question/images/{qst_id}/delete/
    Description: Delete images from a question (only by author or staff)
    Authentication: Required
    Parameters: qst_id (integer) - Question ID
    Request Body: {"images_ids": [1,2,3]}
    Response: {"details": "the images have been deleted successfully"}
    """
    question = get_object_or_404(Question,id=qst_id)
    if question.author != request.user and not request.user.is_staff:
        return Response({'error': 'You are not the author of this question'},status=status.HTTP_403_FORBIDDEN)
    images_ids = request.data.get('images_ids',[])
    
    if not images_ids:
        return Response({'success': 'No images selected for deletion'}, status=status.HTTP_200_OK)
    try:
        images_ids = [int(id) for id in images_ids]
    except:
        raise ValidationError('your images_ids did not respect the format List[int]')

    images_to_delete = ImageQuestion.objects.filter(id__in=images_ids)

    for image in images_to_delete:
        image.img.delete(save=False)
        image.delete()
    return Response({'details':'the images have been deleted successfully'},status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reply_images(request,reply_id):
    """
    Endpoint: DELETE /resources/reply/images/{reply_id}/delete/
    Description: Delete images from a reply (only by author or staff)
    Authentication: Required
    Parameters: reply_id (integer) - Reply ID
    Request Body: {"images_ids": [1,2,3]}
    Response: {"details": "the images have been deleted successfully"}
    """
    reply = get_object_or_404(Reply,id=reply_id)
    if reply.author != request.user and not request.user.is_staff:
        return Response({'error': 'You are not the author of this reply'},status=status.HTTP_403_FORBIDDEN)
    images_ids = request.data.get('images_ids',[])
    if not images_ids:
        return Response({'success': 'No images selected for deletion'}, status=status.HTTP_200_OK)

    try:
        images_ids = [int(id) for id in images_ids]
    except:
        raise ValidationError('your images_ids did not respect the format List[int]')
    
    images_to_delete = ImageReply.objects.filter(id__in=images_ids)

    for image in images_to_delete:
        image.img.delete(save=False)
        image.delete()
    return Response({'details':'the images have been deleted successfully'},status=status.HTTP_204_NO_CONTENT)