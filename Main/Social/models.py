from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from Post.models import Post

class Comment(models.Model):
    description = models.CharField(max_length=250, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published', default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published', default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


