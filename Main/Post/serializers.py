from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from Account.serializers import PersonInfoSerializer
from Social.models import Like


class PostSerializer(serializers.ModelSerializer):
    profile = PersonInfoSerializer(required=True)
    isLiked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'isLiked', 'profile', 'description', 'likeNumber', 'commentNumber', 'image', 'date')

    def get_isLiked(self, obj):
        if (Like.objects.filter(user=obj.user, post=obj.id).exists()):
            return True
        else:
            return False


class BoardSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    #posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)
    #posts = serializerMethodField('get_limited')

    class Meta:
        model = Board
        fields = ('title', 'postNumber', 'posts')


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'user', 'profile', 'description', 'likeNumber', 'commentNumber', 'image', 'date')

