from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class Post(models.Model):
    description = models.CharField(max_length=250, null=True)
    likenumber = models.IntegerField(default=0)
    commentnumber = models.IntegerField(default=0)
    date = models.DateTimeField('date published')
    


class PicPost(models.Model):
    picAdress = models.ImageField(upload_to="")
    person = models.ForeignKey(Post,on_delete=models.CASCADE)

