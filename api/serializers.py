from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password':{'write_only': True, 'required': True }}

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'bio', 'profile_picture')

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'userprofile', 'image')