from rest_framework import serializers
from .models import Tag, TagPost
from Post.serializers import *
from Account.models import *


class TagSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'searchCount')


class TagPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = TagPost
        fields = ('tag', 'post')


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('name', 'bio', 'followerNumber',
                  'followingNumber', 'postNumber',
                  'phoneNumber', 'username'
                  )
