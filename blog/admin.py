from django.contrib import admin

# Register your models here.
from .models import User, BlogArticle, UserBlog, BlogTag, BlogCategory, BlogUpAndDown, BlogComment,Banner

admin.site.register(User)
admin.site.register(UserBlog)
admin.site.register(BlogTag)
admin.site.register(Banner)
admin.site.register(BlogUpAndDown)
admin.site.register(BlogArticle)
admin.site.register(BlogCategory)
admin.site.register(BlogComment)
