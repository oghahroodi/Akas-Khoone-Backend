from django.urls import path
from Core import profileInfoViews,profilePostViews

urlpatterns = [
    path('info/',profileInfoViews.sendInfo),
    path('posts/',profilePostViews.sendPosts),
    # re_path(r'^post/$', postViews.post_list),
    # re_path(r'^post/(?P<pk>[0-9]+)/$', postViews.post_detail),
]