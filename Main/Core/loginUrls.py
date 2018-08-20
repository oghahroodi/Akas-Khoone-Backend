from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.urls import path
urlpatterns = [
    #returns jwt_token
    path("", obtain_jwt_token, name='login'),
    path('refresh/', refresh_jwt_token, name='refresh'),
]