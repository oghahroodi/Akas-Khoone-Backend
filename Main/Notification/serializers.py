from rest_framework import serializers
from .models import Notif
from Account.serializers import *
from Post.serializers import *


class NotifSerializer(serializers.ModelSerializer):
    doer = PersonInfoSerializer(required=True)
    entity = PostSerializer(required=True)

    class Meta:
        model = Notif
        fields = ('kind', 'doer', 'entity', 'date', 'user')
