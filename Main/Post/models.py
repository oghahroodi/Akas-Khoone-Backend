from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from Account.models import Person

class Post(models.Model):
    description = models.CharField(max_length=250, null=True)
    likeNumber = models.IntegerField(default=0)
    commentNumber = models.IntegerField(default=0)
    date = models.DateTimeField('date published', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    profile = models.ForeignKey(Person, on_delete=models.CASCADE)

    def getID(self):
        return self.id

    def getUserID(self):
        return self.user.id

    def increamentLike(self):
        self.likeNumber += 1
        return

    def decrease(self):
        self.likeNumber += -1
        return

    def increamentComment(self):
        self.commentNumber += 1
        return

class Tag(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    searchCount = models.IntegerField(default=0)

    def returnID(self):
        return self.id

    def incrementSearchCount(self):
        self.searchCount += 1
        return


class TagPost(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def returnPost(self):
        return self.post.id


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=100, null=False)
    postNumber = models.IntegerField(default=0)
    posts = models.ManyToManyField(Post, blank=True)

class BoardPost(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
