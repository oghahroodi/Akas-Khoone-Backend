from rest_framework import serializers
from Core.models import Post,Person


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('description', 'likeNumber', 'commentNumber', 'date', 'person')

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('name', 'bio', 'followerNumber', 'followingNumber', 'postNumber', 'username', 'picAddress')
