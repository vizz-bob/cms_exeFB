import csv
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from .models import Lead, ChatbotLead, WebsiteLead, NewsletterSubscriber, LeadShareHistory

# --- CSV Export Action ---
def export_to_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_to_csv.short_description = "Export Selected to CSV"

# --- CHATBOT LEAD ---
@admin.register(ChatbotLead)
class ChatbotLeadAdmin(admin.ModelAdmin):
    # Added 'status' to display and filters
    list_display = ("name", "email", "phone", "status", "display_service", "display_date")
    search_fields = ("name", "email", "phone")
    list_filter = ("status", "service", "created_at")
    # Make status editable directly in the list
    list_editable = ("status",)
    actions = [export_to_csv]

    @admin.display(description='Service')
    def display_service(self, obj):
        return format_html('<b style="color:#1565c0">{}</b>', obj.service or "-")

    @admin.display(description='Date')
    def display_date(self, obj):
        return obj.created_at.strftime("%d %b %Y, %H:%M")

# --- WEBSITE LEAD ---
@admin.register(WebsiteLead)
class WebsiteLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "status", "service", "created_at")
    search_fields = ("name", "email", "company")
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    actions = [export_to_csv]

# --- ALL LEADS ---
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "source", "status", "service", "created_at")
    list_filter = ("status", "source", "created_at")
    list_editable = ("status",)
    actions = [export_to_csv]

# --- NEWSLETTER ---
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active',)
    actions = [export_to_csv]

# --- SHARE HISTORY ---
@admin.register(LeadShareHistory)
class LeadShareHistoryAdmin(admin.ModelAdmin):
    list_display = ('lead', 'recipient_name', 'recipient_phone', 'shared_by', 'shared_at')
    list_filter = ('shared_at', 'platform')