from . import views
from django.urls import path

urlpatterns = [
    path('profile/posts/<int:pk>', views.ProfilePosts.as_view()),
    path('profile/boards/<int:pk>/', views.ProfileBoards.as_view()),
    path('board/<int:boardid>/', views.BoardDetails.as_view()),
    path('post/<int:pk>/', views.PostDetails.as_view()),
    path('home/posts/', views.HomePosts.as_view()),
]