# backend/context_processors.py

from django.contrib.auth import get_user_model
from django.db.models.fields.files import FieldFile

# Yeh function profile image URL ko template context mein daalta hai
def user_avatar_context(request):
    """
    Fetches the user's profile image URL and injects it into the template 
    context under the 'user_avatar' key for Jazzmin display.
    """
    # Check if user is logged in
    if not request.user.is_authenticated:
        return {}

    # Try fetching the profile image URL
    try:
        from core.models import UserProfile # Import local model
        profile = request.user.userprofile
        
        # Check if a file is actually uploaded and return its URL
        if profile.image and isinstance(profile.image, FieldFile):
            return {'user_avatar': profile.image.url}
    
    except Exception:
        # If profile doesn't exist or any other error occurs, return a default.
        pass

    # Jazzmin default icon use karega agar 'user_avatar' key nahi mili ya None return hua.
    return {'user_avatar': None}