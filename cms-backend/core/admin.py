from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin # UserAdmin import karo
from .models import ExampleModel, Theme, UserProfile # UserProfile import karo

admin.site.register(ExampleModel)
admin.site.register(Theme)

# --- NEW: INLINE ADMIN FOR USER PROFILE ---
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Picture & Details'

# Default User admin ko unregister karo
admin.site.unregister(User)

# Custom User admin banao jismein Profile inline ho
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    # list_display me extra field dikha sakte hain, lekin profile picture Jazzmin khud uthayega.