from rest_framework import serializers
from .models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

    def update(self, instance, validated_data):   #prevent the user to change the field
        instance.name = validated_data.get('name', instance.name)
        instance.coef = validated_data.get('coef', instance.coef)
        instance.save()
        return instance