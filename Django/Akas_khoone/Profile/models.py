from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


#should be on top of Person

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    Name = models.CharField(max_length=100, null=False)
    Bio = models.CharField(max_length=250, null=True)
    FollowerNumber = models.IntegerField(default=0)
    FollowingNumber = models.IntegerField(default=0)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    PhoneNumber = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    validation = models.BooleanField(default=False)
    AcountCreationDate = models.DateTimeField('date published')
    


class Pic(models.Model):
    PicAdress = models.ImageField(upload_to="")
    person = models.ForeignKey(Person,on_delete=models.CASCADE)



