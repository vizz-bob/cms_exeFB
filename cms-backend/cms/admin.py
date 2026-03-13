from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import (
    SiteContent, Page,
    HomeContent, AboutContent, ServicesContent,
    ContactContent, CareersContent, ResourcesContent,
    CaseStudy, Resource, Service, ServiceSubService, # <--- Added ServiceSubService
    FooterContent
)

# 1. Page Admin
@admin.register(Page)
class PageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'slug', 'page_order')
    list_editable = ('page_order',) 
    search_fields = ('title', 'slug')
    ordering = ('page_order',)
    
    fieldsets = (
        (None, {'fields': ('title', 'slug')}),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'keywords'),
            'classes': ('collapse',),
        }),
    )

# 2. Base Content Admin
class BaseContentAdmin(admin.ModelAdmin):
    list_display = ('section_label', 'title', 'content_preview', 'image_preview', 'last_updated')
    list_display_links = ('section_label',)
    list_editable = ('title',)
    search_fields = ('title', 'content', 'section_name')
    ordering = ('content_order',)
    list_per_page = 50 
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def section_label(self, obj):
        return format_html(
            '<span style="font-weight:bold; color:#2c3e50;">{}</span><br><span style="font-size:10px; color:#7f8c8d;">{}</span>', 
            obj.section_name, obj.section
        )
    section_label.short_description = "Page Section"
    
    def content_preview(self, obj):
        if not obj.content:
            return "-"
        return (obj.content[:75] + '...') if len(obj.content) > 75 else obj.content
    content_preview.short_description = "Content Preview"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image"

    def last_updated(self, obj):
        return obj.updated_at.strftime("%d %b, %H:%M")
    last_updated.short_description = "Updated"

    readonly_fields = ('page', 'section_name', 'section', 'updated_at')
    fieldsets = (
        ('Edit Content', {
            'fields': ('title', 'content', 'image'),
            'description': 'Update the text or image for this section.'
        }),
        ('Technical Info (Read-Only)', {
            'fields': ('page', 'section_name', 'section', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# 3. Specific Page Admins
@admin.register(HomeContent)
class HomeContentAdmin(BaseContentAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(page='home').order_by('content_order')

@admin.register(AboutContent)
class AboutContentAdmin(BaseContentAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(page='about').order_by('content_order')

@admin.register(ServicesContent)
class ServicesContentAdmin(BaseContentAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(page='services').order_by('content_order')

@admin.register(ContactContent)
class ContactContentAdmin(BaseContentAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(page='contact').order_by('content_order')

@admin.register(CareersContent)
class CareersContentAdmin(BaseContentAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(page='careers').order_by('content_order')

@admin.register(ResourcesContent)
class ResourcesContentAdmin(BaseContentAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(page='resources').order_by('content_order')

@admin.register(FooterContent)
class FooterContentAdmin(BaseContentAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(page='footer').order_by('content_order')

# 4. Master Admin
@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('page', 'section_name', 'title', 'updated_at')
    list_filter = ('page',)
    search_fields = ('title', 'section_name')

# 5. Other Models
@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'created_at')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'created_at')
    list_filter = ('type',)

# --- SERVICE ADMIN with INLINE SUB-SERVICES ---
class ServiceSubServiceInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ServiceSubService
    extra = 1
    fields = ('title', 'description', 'order')

@admin.register(Service)
class ServiceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceSubServiceInline]
    ordering = ('order',)