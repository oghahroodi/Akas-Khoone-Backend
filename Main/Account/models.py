from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100, null=False)
    bio = models.CharField(max_length=250, null=True)
    followerNumber = models.IntegerField(default=0)
    followingNumber = models.IntegerField(default=0)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phoneNumber = models.CharField(validators=[
                                   phone_regex], max_length=17, blank=True,  unique=True)  # validators should be a list
    validation = models.BooleanField(default=False)
    accountCreationDate = models.DateTimeField(
        'date published', default=timezone.now)
    user_regex = RegexValidator(
        regex=r"^[a-zA-Z0-9_.]*$", message="Username can only contain numbers,charachters, _ and .")
    username = models.CharField(
        validators=[user_regex], max_length=100, null=False, unique=True)
    postNumber = models.IntegerField(default=0)
    #profileImage = models.ImageField(upload_to='images/%Y/%m/%d/')

    # store path of images to database for performance
    #picAddress = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.username


class Relation(models.Model):
    userFollowing = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', null=False)
    userFollowed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed', null=False)
