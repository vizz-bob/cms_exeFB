from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ThemeSettingDetail(APIView):
    """
    Static fallback for theme settings since dynamic theming is disabled.
    Prevents frontend crashes if it still tries to fetch this endpoint.
    """
    def get(self, request):
        return Response({
            "name": "Hardcoded Theme",
            "primary_color": "#4338ca",   # Indigo
            "secondary_color": "#8b5cf6", # Violet
            "accent_color": "#f43f5e",    # Rose
            "background_color": "#ffffff",
            "text_color": "#0f172a",
            "chatbot_welcome_message": "Hello! How can I help you?",
            "logo": None 
        }, status=status.HTTP_200_OK)