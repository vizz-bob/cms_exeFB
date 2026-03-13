from rest_framework import viewsets
from .models import LegalPage, LegalPageSection
from .serializers import LegalPageSerializer, LegalPageSectionSerializer

class LegalPageViewSet(viewsets.ModelViewSet):
    """
    CRUD for Legal Pages (Title, Description).
    Lookup by Slug (e.g., /api/legal/pages/privacy-policy/)
    """
    queryset = LegalPage.objects.all()
    serializer_class = LegalPageSerializer
    lookup_field = 'slug'

class LegalPageSectionViewSet(viewsets.ModelViewSet):
    """
    CRUD for Legal Page Sections (Heading, Content).
    """
    queryset = LegalPageSection.objects.all().order_by('order')
    serializer_class = LegalPageSectionSerializer
    filterset_fields = ['legal_page'] # Allows filtering sections by page ID