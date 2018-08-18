from django.db import models
from Profile.models import Person
# Create your models here.



class Post(models.Model):
    Description = models.CharField(max_length=250)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    LikeNumber = models.IntegerField(default=0)
    CommentNumber = models.IntegerField(default=0)
    Date = models.DateTimeField('date published')


class Pic(models.Model):
    PicAdress = models.ImageField(upload_to="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Tag (models.Model):
    info = models.CharField(max_length=150)


class Tag_Post(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)