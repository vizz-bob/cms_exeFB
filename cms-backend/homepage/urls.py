from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomePageDataView, 
    HomePageContentViewSet, 
    TrustedClientViewSet, 
    ProcessStepViewSet, 
    TestimonialViewSet, 
    FAQViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()

# Note: These route names must match the 'resource' prop in your React HomeManager.jsx
router.register(r'homepage-content', HomePageContentViewSet)
router.register(r'clients', TrustedClientViewSet)
router.register(r'process-steps', ProcessStepViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'faqs', FAQViewSet) 

urlpatterns = [
    # The big aggregated object for the frontend Home.jsx
    path('homepage-data/', HomePageDataView.as_view(), name='homepage-data'),
    
    # The CRUD endpoints for HomeManager.jsx
    path('', include(router.urls)),
]