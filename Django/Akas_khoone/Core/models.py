# import jwt

# from datetime import datetime, timedelta

# from django.conf import settings
# from django.contrib.auth.models import (
#     AbstractBaseUser, BaseUserManager, PermissionsMixin
# )
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
# import re

# class UserManager(BaseUserManager):

#     def create_user(self, username, email, password=None):

#         if username is None:
#             raise TypeError('100')

#         if len(username)>30 or len(username)<3:
#             raise TypeError('101')

#         if email is None:
#             raise TypeError('102')

#         if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             raise TypeError('103')
        
#         if password==None :
#             raise TypeError('104')

#         user = self.model(username=username, email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()

#         return user

#     def create_superuser(self, username, email, password):
#         if password is None:
#             raise TypeError('104')

#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#         return user



# class User(AbstractBaseUser, PermissionsMixin):
   
#     username = models.CharField(max_length=30, unique=True)

#     email = models.EmailField(unique=True)

#     is_active = models.BooleanField(default=True)

#     is_staff = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)

#     updated_at = models.DateTimeField(auto_now=True)

#     name = models.CharField(max_length=100)

#     Bio = models.CharField(max_length=250, null=True)

#     FollowerNumber = models.IntegerField(default=0)
    
#     FollowingNumber = models.IntegerField(default=0)
    
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
#     PhoneNumber = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    
#     validation = models.BooleanField(default=False)
    
#     AcountCreationDate = models.DateTimeField('date published')

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     objects = UserManager()

#     def _generate_jwt_token(self):
       
#         dt = datetime.now() + timedelta(days=60)

#         token = jwt.encode({
#             'id': self.pk,
#             'exp': int(dt.strftime('%s'))
#         }, settings.SECRET_KEY, algorithm='HS256')

#         return token.decode('utf-8')
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
    Username = models.CharField(max_length=100,null=False)



class Pic(models.Model):
    PicAdress = models.ImageField(upload_to="")
    person = models.ForeignKey(Person,on_delete=models.CASCADE)



