from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import ResourcesHero, SectionTitles, CaseStudy, DownloadableResource, UsefulLink

@admin.register(ResourcesHero)
class ResourcesHeroAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return ResourcesHero.objects.count() == 0

@admin.register(SectionTitles)
class SectionTitlesAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return SectionTitles.objects.count() == 0

@admin.register(CaseStudy)
class CaseStudyAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'client_name', 'result_stat', 'order')

@admin.register(DownloadableResource)
class DownloadableResourceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'order')

@admin.register(UsefulLink)
class UsefulLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'order')
    list_editable = ('order',)