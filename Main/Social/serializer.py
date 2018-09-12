from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'user', 'description', 'post', 'date')

class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('user', 'description', 'post')


class LikeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'post', 'date')

