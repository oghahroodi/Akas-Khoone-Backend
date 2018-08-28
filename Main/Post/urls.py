from . import views
from django.urls import path

urlpatterns = [
    path('profile/posts/', views.ProfilePosts.as_view()),
    ]
