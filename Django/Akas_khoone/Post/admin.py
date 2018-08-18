from django.contrib import admin

from .models import Post,Pic,Tag,Tag_Post

admin.site.register(Post)
admin.site.register(Pic)
admin.site.register(Tag)
admin.site.register(Tag_Post)