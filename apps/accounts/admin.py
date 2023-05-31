# Django Import
from django.contrib import admin

# Project Import
from apps.accounts.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']

admin.site.register(User, UserAdmin)
