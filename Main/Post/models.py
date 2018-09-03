from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    description = models.CharField(max_length=250, null=True)
    likeNumber = models.IntegerField(default=0)
    commentNumber = models.IntegerField(default=0)
    date = models.DateTimeField('date published', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')


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
