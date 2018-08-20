from django.contrib import admin
from .postModels import Post, Tag, TagPost, PicPost
from .personModels import Person, PicPerson

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(TagPost)
admin.site.register(PicPost)
admin.site.register(Person)
admin.site.register(PicPerson)

