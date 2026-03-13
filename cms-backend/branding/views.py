from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import SiteBranding
from .serializers import SiteBrandingSerializer

class SiteBrandingViewSet(viewsets.ModelViewSet):
    queryset = SiteBranding.objects.all()
    serializer_class = SiteBrandingSerializer

    # Special method to retrieve the single active branding
    @action(detail=False, methods=['get'])
    def active(self, request):
        branding = SiteBranding.objects.filter(is_active=True).first()
        if not branding:
            # Create default if none exists
            branding = SiteBranding.objects.create(site_title="My Website", is_active=True)
        
        serializer = self.get_serializer(branding)
        return Response(serializer.data)