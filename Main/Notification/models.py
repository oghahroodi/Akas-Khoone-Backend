from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from Account.models import *
from Post.models import *


class Notif(models.Model):

    kind = models.CharField(max_length=255)
    doer = models.ForeignKey(Person, on_delete=models.CASCADE)
    entity = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    date=models.CharField(max_length = 255)
    user=models.CharField(max_length = 255)

