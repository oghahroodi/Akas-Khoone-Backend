from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(TagPost)
admin.site.register(Board)
admin.site.register(BoardPost)
