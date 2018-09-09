from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
urlpatterns = [
    path('login/',  TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/',  TokenRefreshView.as_view(), name='refresh'),
    path('profile/info/', views.ProfileInfo.as_view()),
    path('profile/info/<int:pk>/', views.OthersProfileInfo.as_view()),
    path('register/completion/', views.CreateUser.as_view()),
    path('register/initial/', views.CheckUsername.as_view()),
    path('profile/settings/', views.ChangePassword.as_view()),
    path('checkcontacts/', views.CheckContacts.as_view()),
    path('accept/', views.Accept.as_view()),
    path('followers/<int:pk>/<searched>/', views.Followers.as_view()),
    path('followings/<int:pk>/<searched>/', views.Followings.as_view()),
    path('unfollow/', views.Unfollow.as_view()),
    path('passwordforget/firstpage/', views.ForgetPasswordEmail.as_view()),
    path('verification/<str:token>/', views.validation),
    ]