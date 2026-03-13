from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    ServiceHero, ServiceProcess, ServiceFeature, 
    ServiceTestimonial, ServiceFAQ, ServiceCTA
)
from .serializers import (
    ServiceHeroSerializer, ServiceProcessSerializer, ServiceFeatureSerializer, 
    ServiceTestimonialSerializer, ServiceFAQSerializer, ServiceCTASerializer
)
# CMS App se Service List laane ke liye
from cms.models import Service
from cms.serializers import ServiceSerializer

# --- 1. Public Data View (Read Only) ---
class ServicePageDataView(APIView):
    def get(self, request):
        # Use get_or_create to prevent null errors
        hero, _ = ServiceHero.objects.get_or_create(id=1)
        cta, _ = ServiceCTA.objects.get_or_create(id=1)
        
        return Response({
            "hero": ServiceHeroSerializer(hero, context={'request': request}).data,
            "process": ServiceProcessSerializer(ServiceProcess.objects.all(), many=True, context={'request': request}).data,
            "features": ServiceFeatureSerializer(ServiceFeature.objects.all(), many=True, context={'request': request}).data,
            "testimonials": ServiceTestimonialSerializer(ServiceTestimonial.objects.all(), many=True, context={'request': request}).data,
            "faq": ServiceFAQSerializer(ServiceFAQ.objects.all(), many=True, context={'request': request}).data,
            "cta": ServiceCTASerializer(cta, context={'request': request}).data,
            
            # The actual services from the CMS app
            "services_list": ServiceSerializer(Service.objects.all().order_by('order'), many=True, context={'request': request}).data
        })

# --- 2. Admin CRUD ViewSets ---

class ServiceHeroViewSet(viewsets.ModelViewSet):
    queryset = ServiceHero.objects.all()
    serializer_class = ServiceHeroSerializer

class ServiceProcessViewSet(viewsets.ModelViewSet):
    queryset = ServiceProcess.objects.all()
    serializer_class = ServiceProcessSerializer

class ServiceFeatureViewSet(viewsets.ModelViewSet):
    queryset = ServiceFeature.objects.all()
    serializer_class = ServiceFeatureSerializer

class ServiceTestimonialViewSet(viewsets.ModelViewSet):
    queryset = ServiceTestimonial.objects.all()
    serializer_class = ServiceTestimonialSerializer

class ServiceFAQViewSet(viewsets.ModelViewSet):
    queryset = ServiceFAQ.objects.all()
    serializer_class = ServiceFAQSerializer

class ServiceCTAViewSet(viewsets.ModelViewSet):
    queryset = ServiceCTA.objects.all()
    serializer_class = ServiceCTASerializer