from rest_framework import serializers
from Core.postModels import Post


class PostSerializer(serializers.ModelSerializer):

    #Post model fields
    class Meta:
        model = Post
        fields = ('description', 'likeNumber', 'commentNumber', 'date', 'person')

