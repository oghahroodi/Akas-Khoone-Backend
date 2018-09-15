from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ('userFollowing', 'userFollowed')


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = ('userFollowing', 'userFollowed', 'date')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_password(self, value):
        if validators.validate_password(value) is None:
            return value




class PersonFollowPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('username', 'phoneNumber',)


class PersonInfoSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    isfollowed = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = ('username', 'email', 'name', 'bio', 'followerNumber',
                  'followingNumber', 'postNumber', 'boardNumber', 'profileImage','id','isfollowed')
        # , 'profileImage'

    def get_email(self, obj):
        user = User.objects.get(id=obj.user.id)
        return user.username
        
    def get_isfollowed(self,obj):
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



class PersonChangeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('name', 'bio', 'phoneNumber', 'profileImage')
    


class PersonSerializer(serializers.ModelSerializer):


    class Meta:
        model = Person
        fields = ('user', 'name', 'bio', 'followerNumber',
                  'followingNumber', 'postNumber',
                  'phoneNumber', 'username', 'profileImage'
                  )
