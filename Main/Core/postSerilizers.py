<<<<<<< HEAD
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
        fields = ('id', 'description', 'likeNumber', 'commentNumber', 'date',)

=======
#create post serilizers
>>>>>>> 0392953419b3dea0b84147d9bd65b2bca02c007d
