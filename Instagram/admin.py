from django.contrib import admin
from Instagram.models import Post, InstagramUser, Like, UserConnection

# Register your models here.
admin.site.register(Post)
admin.site.register(InstagramUser)
admin.site.register(Like)
admin.site.register(UserConnection)