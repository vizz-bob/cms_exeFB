from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin # <--- This was missing
from .models import AboutPage, TeamMember, Award, TechStack

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return AboutPage.objects.count() == 0

@admin.register(TeamMember)
class TeamMemberAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'year')

@admin.register(TechStack)
class TechStackAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'icon_name', 'order')
    list_editable = ('icon_name', 'order')