from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Ajoute notre champ 'user_type' aux formulaires de création et de modification
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Rôle Utilisateur', {'fields': ('user_type',)}),
    )
    
    # Ajoute 'user_type' à la liste des colonnes affichées dans la liste des utilisateurs
    list_display = ['username', 'email', 'user_type', 'is_staff']

# Enregistre notre modèle CustomUser avec notre configuration personnalisée
admin.site.register(CustomUser, CustomUserAdmin)
