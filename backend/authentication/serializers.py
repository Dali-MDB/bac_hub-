from rest_framework import serializers
from main.models import User,Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        #we don't want to change the password
        password = validated_data.pop('password',None)
        for key,value in validated_data.items():
            setattr(instance,key,value)
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user_ser = UserSerializer(data=user_data)
        
        if user_ser.is_valid():
            user = user_ser.save()
            profile = Profile.objects.create(**validated_data,user = user)
            return profile
        else:
        
            raise serializers.ValidationError(user_ser.errors)

    def update(self, instance, validated_data):
        #we don't want to change the user field
        user_data = validated_data.pop('user',None)
        if user_data:
            user_ser = UserSerializer(instance.user,data=user_data,partial=True)
        
            user_ser.is_valid(raise_exception=True)
            user_ser.save()

        for key,value in validated_data.items():
            setattr(instance,key,value)
        instance.save()
        return instance
        