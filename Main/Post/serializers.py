from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('user', 'description', 'likeNumber', 'commentNumber', 'image')

