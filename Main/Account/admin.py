from django.contrib import admin
from .models import  Person, Relation, FollowRequest

admin.site.register(Person)
admin.site.register(Relation)
admin.site.register(FollowRequest)
