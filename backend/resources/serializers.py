from rest_framework import serializers
from main.models import Resource,Question,Reply,ImageQuestion,ImageReply

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class ImageQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageQuestion
        fields = '__all__'


class ImageReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageReply
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    images = ImageQuestionSerializer(many=True,read_only=True)
    class Meta:
        model = Question
        fields = ["id","content","date_posted","reports","author","subject","images"]
        extra_kwargs = {
            'date_posted': {'read_only': True},
            'reports': {'read_only': True},
            'images' : {'read_only':True}
        }

    def update(self, instance, validated_data):
        subject = validated_data.pop('subject',None)   #the subject can't be changed
        return super().update(instance, validated_data)

class ReplySerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    images = ImageReplySerializer(many=True,read_only=True)
    class Meta:
        model = Reply
        fields = ['id','content','date_posted','reports','replies','parent','author','question','images']
        extra_kwargs = {
            'date_posted': {'read_only': True},
            'reports': {'read_only': True},
            'replies' : {'read_only':True},
            'images' : {'read_only':True}
        }

    def get_replies(self,obj):
        replies = Reply.objects.filter(parent=obj)
        return ReplySerializer(replies,many=True).data
    
    def update(self, instance, validated_data):
        #pop parent and question if existing
        subject = validated_data.pop('subject',None)   
        parent = validated_data.pop('parent',None)   #the subject can't be changed
        return super().update(instance, validated_data)


