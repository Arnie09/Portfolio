from django.contrib import admin
from .models import BlogPost, Category
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(BlogPost, BlogAdmin)
admin.site.register(Category)
