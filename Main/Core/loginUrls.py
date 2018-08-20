from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from . import personView
urlpatterns = [
    #returns jwt_token
    path("", obtain_jwt_token, name='login'),
]