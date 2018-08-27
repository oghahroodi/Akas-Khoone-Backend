from rest_framework import serializers
from Core.models import *
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_password(self, value):
        if validators.validate_password(value) is None:
            return value

    #def validate_username(self,value):


    # def save(self, **kwargs):
    #     user = User(username=self.validated_data['username'])
    #     if validators.validate_password(self.validated_data['password'], user):
    #         user.set_password(self.validated_data['password'])
    #         user.save()
    #         return user


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('user', 'description', 'likeNumber', 'commentNumber', 'image')


class PersonSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = Person
        fields = ('user', 'name', 'bio', 'followerNumber',
                  'followingNumber', 'postNumber',
                  'phoneNumber', 'username'
                  )
        #, 'profileImage'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            person, created = Person.objects.update_or_create(user=user, **validated_data)
            return person

