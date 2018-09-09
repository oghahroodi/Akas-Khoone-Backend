from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from Account.serializers import PersonInfoSerializer
from Account.models import Relation
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
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ('id', 'title', 'postNumber', 'posts')

    def get_posts(self, obj):
        pk = self.context.get('pk')
        usersAllowed = [i.followed() for i in Relation.objects.filter(userFollowing__id=pk)]
        usersAllowed.append(pk)
        queryset = obj.posts.filter(user__in=usersAllowed)[:5]
        return PostSerializer(instance=queryset, many=True).data


class CreateBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('user','title', 'postNumber', 'posts')


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'user', 'profile', 'description', 'likeNumber', 'commentNumber', 'image', 'date')



