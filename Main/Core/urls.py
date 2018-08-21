from django.contrib import admin
from django.urls import path,include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from . import views


urlpatterns = [
    path('login/',  obtain_jwt_token, name='login'),
    path('login/refresh/',  refresh_jwt_token, name='refresh'),
    path('profile/info/', views.SendInfo.as_view()),
    path('profile/posts/', views.SendPosts.as_view()),
]