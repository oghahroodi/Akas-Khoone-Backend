from rest_framework import serializers

from .personModels import Person

from django.contrib.auth import authenticate

class PersonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Person
        fields = ('name', 'bio', 'followerNumber', 'followingNumber', 'postNumber', 'username', 'picAddress')