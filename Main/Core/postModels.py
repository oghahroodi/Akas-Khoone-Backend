from .personModels import Person
from django.db import models
from django.core.validators import RegexValidator

#table for post
class Post(models.Model):
    description = models.CharField(max_length=250, null=True)
    likeNumber = models.IntegerField(default=0)
    commetNumber = models.IntegerField(default=0)
    date = models.DateTimeField('date published')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    #store path of images to database for performance
    picAdress = models.CharField(max_length=200, null=False, unique=True)


#table for tag
class Tag(models.Model):
    info = models.CharField(max_length=255, null=False, unique=True)

#table for conect tag to post
class TagPost(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


