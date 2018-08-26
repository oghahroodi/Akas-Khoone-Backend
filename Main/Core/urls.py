from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from . import views
urlpatterns = [
    path('login/',  TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/',  TokenRefreshView.as_view(), name='refresh'),
    path('profile/info/', views.ProfileInfo.as_view()),
    path('profile/posts/', views.ProfilePosts.as_view()),
    path('contacts/', views.SendContactPerson.as_view()),
    path('register/completion/', views.CreateUser.as_view()),
    path('register/initial/', views.CheckUsername.as_view()),
]