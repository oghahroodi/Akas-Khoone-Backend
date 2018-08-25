from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from . import views


urlpatterns = [
    path('login/',  TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/',  TokenRefreshView.as_view(), name='refresh'),
    path('profile/info/', views.sendInfo.as_view()),
    path('profile/posts/', views.SendPosts.as_view()),
    path('contacts/', views.SendContactPerson.as_view()),
]