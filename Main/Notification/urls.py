from django.urls import path

from . import views
urlpatterns = [
    path('follow/', views.SearchTags),
]