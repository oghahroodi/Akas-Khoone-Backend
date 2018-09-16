from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
urlpatterns = [
    path('login/',  TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/',  TokenRefreshView.as_view(), name='refresh'),
    path('profile/info/<int:pk>/', views.ProfileInfo.as_view()),
    path('register/completion/', views.CreateUser.as_view()),
    path('register/initial/', views.CheckUsername.as_view()),
    path('profile/settings/', views.ChangePassword.as_view()),
    path('checkcontacts/', views.CheckContacts.as_view()),
    path('accept/<int:pk>/', views.Accept.as_view()),
    path('reject/<int:pk>/', views.Reject.as_view()),
    path('subfollow/<int:pk>/', views.SubFollow.as_view()),
    path('followers/<int:pk>/<searched>/', views.Followers.as_view()),
    path('followings/<int:pk>/<searched>/', views.Followings.as_view()),
    path('unfollow/', views.Unfollow.as_view()),
    path('passwordforget/firstpage/', views.ForgetPasswordEmail.as_view()),
    path('passwordforget/secondpage/', views.ForgetPasswordTokenCheck.as_view()),
    path('passwordforget/lastpage/', views.ForgetPasswordNewPassword.as_view()),
    path('verification/<str:token>/', views.validation),
    path('getid', views.GetID.as_view()),
    path('invitation/', views.FriendInvite.as_view()),
    path('follow/<int:pk>/', views.Follow.as_view()),
    ]