from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Rôle Utilisateur', {'fields': ('user_type',)}),
    )
    
    list_display = ['username', 'email', 'user_type', 'is_staff']
admin.site.register(CustomUser, CustomUserAdmin)
