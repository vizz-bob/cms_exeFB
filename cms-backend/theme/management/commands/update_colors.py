from django.core.management.base import BaseCommand
from theme.models import ThemeSetting

class Command(BaseCommand):
    help = 'Updates the theme colors to the new palette.'

    def handle(self, *args, **options):
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
            self.stdout.write(self.style.SUCCESS('Successfully updated theme colors.'))
        else:
            self.stdout.write(self.style.WARNING('No ThemeSetting object found.'))
