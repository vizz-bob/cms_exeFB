from django.contrib import admin
from .models import BlogPost, BlogCategory 
from django.utils.text import slugify

# --- 1. ADMIN FOR BLOG CATEGORY (UPDATED) ---
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    # FIX: Add prepopulated_fields to automatically generate slug from name
    prepopulated_fields = {'slug': ('name',)} 
    list_filter = ('name',) # Optional filter added for usability


# --- 2. ADMIN FOR BLOG POST (Existing setup) ---
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the BlogPost model.
    """
    # list_display is updated in your previous step to include category
    list_display = ('title', 'category', 'published', 'created_at')
    list_filter = ('published', 'category', 'created_at')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)