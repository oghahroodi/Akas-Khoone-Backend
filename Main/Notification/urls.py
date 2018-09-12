from django.urls import path
from . import views

from . import views
urlpatterns = [
    path('notification/', views.Notification.as_view()),
    path('getnotification/', views.getNotification.as_view()),
]
