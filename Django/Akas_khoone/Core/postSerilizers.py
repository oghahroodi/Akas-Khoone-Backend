from rest_framework import serializers

from .models import User

from django.contrib.auth import authenticate


class PostSerilizer(serializers.Serializer):
    description = serializers.CharField(max_length=250, null=True)
    likenumber = serializers.IntegerField(default=0)
    commentnumber = serializers.IntegerField(default=0)
    date = serializers.DateTimeField('date published')


    class Meta:
        model = User
        fields = ('description', 'likenumber', 'commentnumber', 'date',)

