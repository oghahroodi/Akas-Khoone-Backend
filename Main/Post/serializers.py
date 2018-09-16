from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from Account.serializers import PersonInfoSerializer
from Account.models import Relation
from Social.models import Like


class PostSerializer(serializers.ModelSerializer):
    isLiked = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'isLiked', 'profile', 'description', 'likeNumber', 'commentNumber', 'image', 'date')

    def get_isLiked(self, obj):
        if (Like.objects.filter(user=obj.user, post=obj.id).exists()):
            return True
        else:
            return False

    def get_profile(self, obj):
        return PersonInfoSerializer(Person.objects.get(user_id=obj.user.id)).data


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


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('user', 'description', 'image')



