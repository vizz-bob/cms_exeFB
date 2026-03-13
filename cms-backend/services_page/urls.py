from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServicePageDataView,
    ServiceHeroViewSet,
    ServiceProcessViewSet,
    ServiceFeatureViewSet,
    ServiceTestimonialViewSet,
    ServiceFAQViewSet,
    ServiceCTAViewSet
)

router = DefaultRouter()
# These names match the 'resource' prop in the React component below
router.register(r'service-hero', ServiceHeroViewSet)
router.register(r'service-process', ServiceProcessViewSet)
router.register(r'service-features', ServiceFeatureViewSet)
router.register(r'service-testimonials', ServiceTestimonialViewSet)
router.register(r'service-faq', ServiceFAQViewSet)
router.register(r'service-cta', ServiceCTAViewSet)

urlpatterns = [
    # Public Data
    path('services-page-data/', ServicePageDataView.as_view(), name='services-page-data'),
    
    # Admin CRUD
    path('', include(router.urls)),
]