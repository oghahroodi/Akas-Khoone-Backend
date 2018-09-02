from rest_framework import serializers
from .models import Tag, TagPost
from Post.serializers import *

class TagSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'searchCount')


class TagPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = TagPost
        fields = ('tag', 'post')
