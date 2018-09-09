from rest_framework import serializers
from .models import *
from Account.serializers import PersonInfoSerializer
from Account.models import Relation


class PostSerializer(serializers.ModelSerializer):
    profile = PersonInfoSerializer(required=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'profile', 'description', 'likeNumber', 'commentNumber', 'date')
        #'image',


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'profile', 'description', 'likeNumber', 'commentNumber', 'date')
        #'image',


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
        fields = ('user', 'title', 'postNumber', 'posts')
