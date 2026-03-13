from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .sections import get_section_slugs
from .models import SiteContent, CaseStudy, Resource, Service, Page, ServiceSubService
from .serializers import (
    SiteContentSerializer, CaseStudySerializer, 
    ResourceSerializer, ServiceSerializer, PageSerializer,
    ServiceSubServiceSerializer
)

@api_view(['GET'])
def get_section_choices(request, page):
    """Returns the allowed section slugs for a given page."""
    sections = get_section_slugs(page)
    return Response(sections)

class SiteContentViewSet(viewsets.ModelViewSet):
    queryset = SiteContent.objects.all()
    serializer_class = SiteContentSerializer

    def get_queryset(self):
        qs = SiteContent.objects.all()
        page = self.request.query_params.get("page")
        if page:
            qs = qs.filter(page=page)
        return qs

@api_view(['GET'])
def home_page_content(request):
    """Returns all the site content for the home page."""
    qs = SiteContent.objects.filter(page="home")
    serializer = SiteContentSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)

# --- EDITABLE VIEWSETS (Changed from ReadOnlyModelViewSet to ModelViewSet) ---

class CaseStudyViewSet(viewsets.ModelViewSet):
    queryset = CaseStudy.objects.all().order_by('-created_at')
    serializer_class = CaseStudySerializer

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all().order_by('-created_at')
    serializer_class = ResourceSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('order')
    serializer_class = ServiceSerializer
    lookup_field = 'slug' # Default for router generation

    def get_object(self):
        """
        Hybrid Lookup:
        - If URL param is an Integer (e.g. /api/services/19/), fetch by ID (for Admin Panel).
        - If URL param is a String (e.g. /api/services/virtual-cfo/), fetch by Slug (for Public Site).
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)

        # 1. Try ID lookup (for Admin Editing)
        if lookup_value and lookup_value.isdigit():
            queryset = self.filter_queryset(self.get_queryset())
            obj = get_object_or_404(queryset, id=lookup_value)
            self.check_object_permissions(self.request, obj)
            return obj

        # 2. Fallback to Slug lookup (for Public Display)
        return super().get_object()

class ServiceSubServiceViewSet(viewsets.ModelViewSet):
    """
    Allows editing sub-points (e.g. 'Statutory Audit' under 'Audit').
    """
    queryset = ServiceSubService.objects.all().order_by('order')
    serializer_class = ServiceSubServiceSerializer

# --- NAVBAR PAGES ---

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all().order_by('page_order')
    serializer_class = PageSerializer