from django.db import models


class PostNotif(models.Model):

    user = models.CharField(max_length=255)
    p = models.CharField(max_length=255)


class LikeNotif(models.Model):
    pass


class FollowNotif(models.Model):
    pass
