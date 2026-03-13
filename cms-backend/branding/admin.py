from django.contrib import admin
from .models import SiteBranding

@admin.register(SiteBranding)
class SiteBrandingAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'is_active', 'updated_at')
    list_editable = ('is_active',)