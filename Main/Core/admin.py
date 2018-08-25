from django.contrib import admin
from .models import Post, Tag, TagPost, Person


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(TagPost)
admin.site.register(Person)
