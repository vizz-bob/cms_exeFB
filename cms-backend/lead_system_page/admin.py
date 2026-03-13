from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import LSHero, LSFeature, LSBottomCTA, LSDashboard # Updated Import

# ... (LSHeroAdmin, LSFeatureAdmin same rahenge) ...

@admin.register(LSHero)
class LSHeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle')
    def has_add_permission(self, request):
        return LSHero.objects.count() == 0

@admin.register(LSFeature)
class LSFeatureAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'icon_name', 'order') 
    list_display_links = ('id',) 
    list_editable = ('title', 'icon_name', 'order')

# --- NEW ADMIN ---
@admin.register(LSDashboard)
class LSDashboardAdmin(admin.ModelAdmin):
    list_display = ('placeholder_text', 'image')
    def has_add_permission(self, request):
        return LSDashboard.objects.count() == 0
# -----------------

@admin.register(LSBottomCTA)
class LSBottomCTAAdmin(admin.ModelAdmin):
    list_display = ('title', 'button_text')
    def has_add_permission(self, request):
        return LSBottomCTA.objects.count() == 0