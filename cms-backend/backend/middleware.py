import datetime
from django.conf import settings

class AutomaticThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Sirf Admin pages par hi logic chalayein taaki performance fast rahe
        if request.path.startswith('/admin/'):
            self.update_theme_based_on_time(request)
        
        response = self.get_response(request)
        return response

    def update_theme_based_on_time(self, request):
        # 1. Current Time Calculate karo (IST)
        IST_OFFSET = datetime.timedelta(hours=5, minutes=30)
        now_utc = datetime.datetime.utcnow()
        now_ist = now_utc + IST_OFFSET
        
        # 6 AM se 6 PM tak Day, baaki Night
        is_daytime = 6 <= now_ist.hour < 18

        # 2. Theme Settings Define karo
        if is_daytime:
            # --- LIGHT MODE (Day) ---
            new_theme = "lux"
            theme_tweaks = {
                "theme": "lux",
                "dark_mode_theme": None,
                "brand_colour": "navbar-light",
                "navbar": "navbar-white",
                "sidebar": "sidebar-light-primary",
                "accent": "accent-info",
                "button_classes": {
                    "primary": "btn-primary",
                    "secondary": "btn-secondary",
                    "info": "btn-info",
                    "warning": "btn-warning",
                    "danger": "btn-danger",
                    "success": "btn-success"
                }
            }
        else:
            # --- DARK MODE (Night) ---
            new_theme = "darkly"
            theme_tweaks = {
                "theme": "darkly",
                "dark_mode_theme": None,
                "brand_colour": "navbar-dark",
                "navbar": "navbar-dark",
                "sidebar": "sidebar-dark-indigo",
                "accent": "accent-warning",
                "button_classes": {
                    "primary": "btn-primary",
                    "secondary": "btn-secondary",
                    "info": "btn-info",
                    "warning": "btn-warning",
                    "danger": "btn-danger",
                    "success": "btn-success"
                }
            }

        # 3. Session Update karo (Jazzmin yahan se read karega)
        current_tweaks = request.session.get('jazzmin_ui_tweaks', {})
        
        # Agar current theme aur time-based theme alag hain, tabhi update karo
        if current_tweaks.get('theme') != new_theme:
            request.session['jazzmin_ui_tweaks'] = theme_tweaks
            request.session.modified = True