from . import views
from django.urls import path

urlpatterns = [
    path('comment/<int:pk>/', views.PostComments.as_view())
    ]
