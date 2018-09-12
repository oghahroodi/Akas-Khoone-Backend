from . import views
from django.urls import path

urlpatterns = [
    path('comment/<int:pk>/', views.PostComments.as_view()),
    path('like/<int:pk>/', views.LikePosts.as_view()),
    path('comment/', views.Comment.as_view()),
    # path('followrequest/', views.FollowRequest.as_view()),
]
