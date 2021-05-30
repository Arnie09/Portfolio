from django.contrib import admin
from .models import ExtendedUser
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(ExtendedUser, UserAdmin)