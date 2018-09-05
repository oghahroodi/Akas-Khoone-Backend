from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'user', 'description', 'likeNumber', 'commentNumber', 'date')
        #'image'


class BoardSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    #posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)
    #posts = serializerMethodField('get_limited')

    class Meta:
        model = Board
        fields = ('title', 'postNumber', 'posts')