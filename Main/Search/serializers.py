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
    isfollowed=serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('name', 'bio', 'followerNumber',
                  'followingNumber', 'postNumber',
                  'phoneNumber', 'username','isfollowed'
                  )

    def get_isfollowed(self, obj):
        followeing = self.context.get('userid')
        followed = Person.objects.get(username=obj.username)
        if (Relation.objects.get(userFollowing_id=followeing, userFollowed= followed.id)):
            return True
        else:
            return False
