from django.contrib import admin
from .postModels import Post, Tag, TagPost
from .personModels import Person

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(TagPost)
admin.site.register(Person)

