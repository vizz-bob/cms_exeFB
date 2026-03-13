from django.contrib import admin
from .models import LegalPage, LegalPageSection

# --- INLINE SECTION (Ye wo Heading & Content wale boxes hain) ---
class SectionInline(admin.StackedInline):
    model = LegalPageSection
    extra = 1  # Bhai, ye '1' zaroori hai taaki ek khali box hamesha dikhe
    fields = ('heading', 'content', 'order')
    ordering = ('order',)
    # classes = ('collapse',)  <-- YE LINE HATA DI HAI (Ab box chupa nahi rahega)

# --- MAIN PAGE ADMIN ---
@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'last_updated')
    search_fields = ('title',)
    
    # Title likhte hi Slug apne aap ban jayega
    prepopulated_fields = {'slug': ('title',)}
    
    # Sections ko yahan jod diya
    inlines = [SectionInline]

    # Layout ko thoda saaf-suthra banate hain
    fieldsets = (
        ("Page Details", {
            "fields": ("title", "slug", "description"),
            "description": "Page ka naam aur chhota sa intro yahan likhein."
        }),
    )