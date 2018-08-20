from django.contrib import admin
<<<<<<< HEAD
from .postModels import Post, PicPost
from .personModels import Person,PicPerson

admin.site.register(Post)
admin.site.register(PicPost)
admin.site.register(PicPerson)
admin.site.register(Person)
# Register your models here.
=======
from .postModels import Post, Tag, TagPost, PicPost
from .personModels import Person, Pic

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(TagPost)
admin.site.register(PicPost)
admin.site.register(Person)
admin.site.register(Pic)
>>>>>>> 0392953419b3dea0b84147d9bd65b2bca02c007d
