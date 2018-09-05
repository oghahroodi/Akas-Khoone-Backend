from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from Account.serializers import PersonInfoSerializer


class PostSerializer(serializers.ModelSerializer):
    profile = PersonInfoSerializer(required=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'profile', 'description', 'likeNumber', 'commentNumber', 'image', 'date')


class BoardSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    #posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)
    #posts = serializerMethodField('get_limited')

    class Meta:
        model = Board
        fields = ('title', 'postNumber', 'posts')