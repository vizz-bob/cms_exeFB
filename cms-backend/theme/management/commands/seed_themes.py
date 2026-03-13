from django.core.management.base import BaseCommand
from theme.models import ThemeSetting

class Command(BaseCommand):
    help = 'Seeds the website theme with a Lighter Color Scheme'

    def handle(self, *args, **kwargs):
        self.stdout.write('🎨 Seeding Lighter Theme...')

        # Lighter Color Scheme (Same Blue/Slate family, but lighter tones)
        theme_data = {
            # Primary: Thoda light Slate (Was #0f172a -> Now #1e293b)
            "primary_color": "#1e293b",   
            
            # Secondary: Brighter Blue (Was #3b82f6 -> Now #60a5fa)
            "secondary_color": "#60a5fa", 
            
            # Accent: Lighter Amber (Was #f59e0b -> Now #fbbf24)
            "accent_color": "#fbbf24",    
            
            # Background: Pure White for cleaner look (Was #f8fafc -> Now #ffffff)
            "background_color": "#ffffff", 
            
            # Text: Softer Slate Gray (Was #334155 -> Now #475569)
            "text_color": "#475569",      
            
            "is_active": True
        }

        # Create or update the singleton theme
        # Using id=1 to ensure we update the main theme record
        ThemeSetting.objects.update_or_create(id=1, defaults=theme_data)

        self.stdout.write(self.style.SUCCESS('🎉 Lighter Theme Applied Successfully!'))