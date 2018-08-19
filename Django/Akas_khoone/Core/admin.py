from django.contrib import admin
from .models import Person, Pic
from .postModels import Post, PicPost

admin.site.register(Person)
admin.site.register(Post)
admin.site.register(Pic)
admin.site.register(PicPost)


