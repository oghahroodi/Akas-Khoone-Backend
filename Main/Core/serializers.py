from rest_framework import serializers
from Core.models import Post, Person
from django.contrib.auth.models import User
from django.utils import timezone

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('description', 'likeNumber', 'commentNumber', 'date', 'person')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class PersonSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = Person
        fields = ('user', 'name', 'bio', 'followerNumber', 'followingNumber', 'postNumber', 'phoneNumber', 'username', 'picAddress')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        person, created = Person.objects.update_or_create(user=user, accountCreationDate=timezone.now(),
                                                          **validated_data)
        return person