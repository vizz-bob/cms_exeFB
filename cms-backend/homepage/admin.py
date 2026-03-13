from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import (
    HomePageContent, TrustedClient, 
    ProcessStep, Testimonial, FAQ
)

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    # Singleton Pattern
    def has_add_permission(self, request):
        return HomePageContent.objects.count() == 0

@admin.register(TrustedClient)
class TrustedClientAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'order')

@admin.register(ProcessStep)
class ProcessStepAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order')

@admin.register(Testimonial)
class TestimonialAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('author_name', 'company', 'order')

@admin.register(FAQ)
class FAQAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('question', 'order')