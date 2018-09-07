from django.contrib import admin
from .models import  PostNotif,LikeNotif,FollowNotif

admin.site.register(PostNotif)
admin.site.register(LikeNotif)
admin.site.register(FollowNotif)
