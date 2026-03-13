from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import (
    ServiceHero, ServiceProcess, ServiceFeature, 
    ServiceTestimonial, ServiceFAQ, ServiceCTA
)

@admin.register(ServiceHero)
class ServiceHeroAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return ServiceHero.objects.count() == 0

@admin.register(ServiceProcess)
class ServiceProcessAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order')

@admin.register(ServiceFeature)
class ServiceFeatureAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'order')

@admin.register(ServiceTestimonial)
class ServiceTestimonialAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'role', 'order')

@admin.register(ServiceFAQ)
class ServiceFAQAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('question', 'order')

@admin.register(ServiceCTA)
class ServiceCTAAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return ServiceCTA.objects.count() == 0