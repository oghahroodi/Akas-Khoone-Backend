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
        fields = ('id', 'name', 'bio', 'followerNumber',
                  'followingNumber', 'postNumber',
                  'phoneNumber', 'username', 'isfollowed', "profileImage"
                  )

    def get_isfollowed(self, obj):
        following = self.context.get('userid')
        try:
            Relation.objects.get(userFollowing=following, userFollowed=obj.user.id)
            return 'following'
        except Relation.DoesNotExist:
            try:
                FollowRequest.objects.get(userFollowing=following, userFollowed=obj.user.id)
                return 'requested'
            except FollowRequest.DoesNotExist:
                return 'notfollowed'
