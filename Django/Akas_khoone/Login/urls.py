from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view,{'template_name': 'template/index.html'}, name='login'),
]