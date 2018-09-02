from . import views
from django.urls import path

urlpatterns = [
    path('profile/posts/', views.ProfilePosts.as_view()),
    path('post/<int:pk>/', views.PostDetails.as_view())
    ]
