from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AboutPageDataView, 
    AboutPageViewSet, 
    TeamMemberViewSet, 
    AwardViewSet, 
    TechStackViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()

# These names must match the 'resource' prop in your React AboutManager.jsx
router.register(r'about-content', AboutPageViewSet)  
router.register(r'team-members', TeamMemberViewSet)
router.register(r'tech-stack', TechStackViewSet)
router.register(r'awards', AwardViewSet)

urlpatterns = [
    # The public endpoint (Read Only)
    path('about-page-data/', AboutPageDataView.as_view(), name='about-page-data'),
    
    # The Admin endpoints (Create, Update, Delete)
    path('', include(router.urls)),
]