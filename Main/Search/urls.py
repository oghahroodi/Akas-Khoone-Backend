from . import views
from django.urls import path, re_path

urlpatterns = [
    re_path(r'^gettagsposts/(?P<tag>[^/]+)/$', views.GetTagsPosts.as_view()),
    path('searchtags/', views.SearchTags.as_view()),
    path('searchusers/',views.SearchUsers.as_view()),
    path('trendingtags/',views.TrendingTags.as_view()),
]