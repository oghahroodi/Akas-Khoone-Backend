from rest_framework import serializers

from .postModels import Post

from django.contrib.auth import authenticate


class PostSerilizer(serializers.Serializer):
    description = serializers.CharField(max_length=250, null=True)
    likeNumber = serializers.IntegerField(default=0)
    commentNumber = serializers.IntegerField(default=0)
    date = serializers.DateTimeField('date published')


    class Meta:
        model = Post
        fields = ('description', 'likeNumber', 'commentNumber', 'date',)

