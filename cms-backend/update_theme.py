import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from theme.models import ThemeSetting

def update_theme_colors():
    theme_setting = ThemeSetting.objects.first()
    if theme_setting:
        # New Light Mode Colors
        theme_setting.light_primary_color = '#2c3e50'
        theme_setting.light_secondary_color = '#ecf0f1'
        theme_setting.light_accent_color = '#3498db'
        theme_setting.light_background_color = '#ffffff'
        theme_setting.light_text_color = '#34495e'
        
        # New Dark Mode Colors
        theme_setting.dark_primary_color = '#ecf0f1'
        theme_setting.dark_secondary_color = '#34495e'
        theme_setting.dark_accent_color = '#3498db'
        theme_setting.dark_background_color = '#2c3e50'
        theme_setting.dark_text_color = '#ecf0f1'
        
        theme_setting.save()
        print("Theme colors updated successfully.")
    else:
        print("No ThemeSetting object found.")

if __name__ == "__main__":
    update_theme_colors()
