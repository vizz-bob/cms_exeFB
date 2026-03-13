from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import ContactMessage, ContactPage, OfficeAddress, Ticket

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'email', 'priority', 'status', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('subject', 'email', 'description')
    list_editable = ('status', 'priority')
    readonly_fields = ('created_at',)

@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    # Group fields for better Admin UX
    fieldsets = (
        ("Hero Section", {
            "fields": ("hero_title", "hero_subtitle")
        }),
        ("Form Configuration", {
            "fields": (
                "form_title", 
                "form_button_text", 
                "is_sub_service_multiselect"
            ),
            "description": "Configure the form title, button text, and selection behavior."
        }),
        ("Form Labels", {
            "fields": (
                "form_name_label", 
                "form_company_label", 
                "form_email_label", 
                "form_phone_label", 
                "form_service_label", 
                "form_timeline_label", 
                "form_message_label"
            ),
            "classes": ("collapse",),
            "description": "Change the display labels for the contact form fields."
        }),
        ("Map & Support", {
            "fields": ("map_embed_url", "support_title", "support_text")
        }),
    )

    def has_add_permission(self, request):
        return ContactPage.objects.count() == 0

@admin.register(OfficeAddress)
class OfficeAddressAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'email', 'order')