from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import ChatbotFlowStep 

# --- THEME SETTING REMOVED FROM ADMIN ---

@admin.register(ChatbotFlowStep)
class ChatbotFlowStepAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('step_order', 'question_text', 'field_to_save', 'is_required')
    list_editable = ('question_text', 'field_to_save', 'is_required')
    ordering = ('step_order',)
    search_fields = ('question_text', 'field_to_save')