from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'website', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'user__username')
    actions = ['approve_companies']

    def approve_companies(self, request, queryset):
        queryset.update(is_approved=True)
    approve_companies.short_description = "Approuver les entreprises sélectionnées"
