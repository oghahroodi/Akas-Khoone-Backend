from .personModels import Person
from django.db import models
from django.core.validators import RegexValidator

class Post(models.Model):
    description = models.CharField(max_length=250, null=True)
    likeNumber = models.IntegerField(default=0)
    commetNumber = models.IntegerField(default=0)
    date = models.DateTimeField('date published')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class PicPost(models.Model):
    picAdress = models.ImageField(upload_to="")
    person = models.ForeignKey(Post,on_delete=models.CASCADE)
