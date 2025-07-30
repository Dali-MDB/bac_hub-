from rest_framework import serializers
from main.models import Resource,Question,Reply,ImageQuestion,ImageReply

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            'date_posted': {'read_only': True},
            'reports': {'read_only': True},
        }

class ReplySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta:
        model = Reply
        fields = ['id','content','date_posted','reports','children','parent','author','question']
        extra_kwargs = {
            'date_posted': {'read_only': True},
            'reports': {'read_only': True},
        }

    def get_children(self,obj):
        children = Reply.objects.filter(parent=obj)
        return ReplySerializer(children,many=True).data


class ImageQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageQuestion
        fields = '__all__'


class ImageReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageReply
        fields = '__all__'
