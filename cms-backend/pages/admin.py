from django.contrib import admin

from .models import PageContent

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    """
    Customizes the appearance of the PageContent model in the Django admin.
    """
    list_display = ('title', 'slug') # Columns to show in the list view
    search_fields = ('title', 'slug') # Adds a search bar for these fields
    
    # Pre-populate the slug field from the title as the user types
    prepopulated_fields = {'slug': ('title',)} 

    fieldsets = (
        (None, {
            'fields': ('title', 'slug')
        }),
        ('Page Body', {
            'fields': ('content',)
        }),
    )
