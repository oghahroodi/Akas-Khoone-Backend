from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100, null=False)
    bio = models.CharField(max_length=250, null=True)
    followerNumber = models.IntegerField(default=0)
    followingNumber = models.IntegerField(default=0)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phoneNumber = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    validation = models.BooleanField(default=False)
    acountCreationDate = models.DateTimeField('date published')
    username = models.CharField(max_length=100,null=False)

class Pic(models.Model):
    PicAdress = models.ImageField(upload_to="")
    person = models.ForeignKey(Person,on_delete=models.CASCADE)