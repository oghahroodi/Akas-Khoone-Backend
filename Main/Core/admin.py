from django.contrib import admin
from .postModels import Post, PicPost
from .personModels import Person,PicPerson

admin.site.register(Post)
admin.site.register(PicPost)
admin.site.register(PicPerson)
admin.site.register(Person)
# Register your models here.
