from django.contrib import admin
from .models import Post, Tag, TagPost
from .models import Person

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(TagPost)
admin.site.register(Person)

