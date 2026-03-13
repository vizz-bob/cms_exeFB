from django.contrib import admin
from django.utils.html import format_html
# from adminsortable2.admin import SortableAdminMixin # Uncomment if installed
from .models import Stakeholder, SolutionsPage

@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'icon_preview', 'desc_preview', 'order')
    list_editable = ('title', 'order') 
    list_display_links = ('id',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

    def desc_preview(self, obj):
        return obj.description[:75] + "..." if obj.description else "-"
    desc_preview.short_description = "Description"

    def icon_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: contain;" />', obj.image.url)
        return "❌ No Image"
    icon_preview.short_description = "Image Preview"

@admin.register(SolutionsPage)
class SolutionsPageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SolutionsPage.objects.exists()