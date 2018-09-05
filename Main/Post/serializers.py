from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from Account.serializers import PersonInfoSerializer


class PostSerializer(serializers.ModelSerializer):
    Profile = PersonInfoSerializer(required=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'Profile', 'description', 'likeNumber', 'commentNumber', 'image', 'date')

