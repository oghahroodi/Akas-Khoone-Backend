from . import views
from django.urls import path

urlpatterns = [
    path('profile/posts/', views.ProfilePosts.as_view()),
    path('profile/boards/', views.ProfileBoards.as_view()),
    path('profile/boards/<int:pk>/', views.ProfileBoardPosts.as_view()),
    path('post/<int:pk>/', views.PostDetails.as_view()),
    path('home/posts/', views.HomePosts.as_view()),
]
