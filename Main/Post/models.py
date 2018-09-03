from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    description = models.CharField(max_length=250, null=True)
    likeNumber = models.IntegerField(default=0)
    commentNumber = models.IntegerField(default=0)
    date = models.DateTimeField('date published', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #image = models.ImageField(upload_to='images/%Y/%m/%d/')


class Tag(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)


class TagPost(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=100, null=False)
    postNumber = models.IntegerField(default=0)


class BoardPost(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

