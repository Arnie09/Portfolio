from django.contrib import admin
from .models import BlogPost
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(BlogPost, BlogAdmin)