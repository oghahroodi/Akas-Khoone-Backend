from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'user', 'description', 'post', 'date')

class CommentCreateSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('user', 'description', 'post','profile')

    def get_profile(self, obj):
        return PersonInfoSerializer(Person.objects.get(user_id=obj.user.id)).data


class LikeCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = Like
        fields = ('user', 'post', 'date')

