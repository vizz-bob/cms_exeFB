from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadSystemPageDataView, LSFeatureViewSet, LSHeroViewSet, LSDashboardViewSet, LSBottomCTAViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'ls-features', LSFeatureViewSet)
# Register other models just in case direct access is needed later
router.register(r'ls-hero', LSHeroViewSet)
router.register(r'ls-dashboard', LSDashboardViewSet)
router.register(r'ls-bottom-cta', LSBottomCTAViewSet)

urlpatterns = [
    # Route for fetching/updating the main page content (Singleton ID=1)
    # Allows 'lead-system-data/' and 'lead-system-data/1/' to work
    path('lead-system-data/', LeadSystemPageDataView.as_view(), name='lead-system-data'),
    path('lead-system-data/<int:pk>/', LeadSystemPageDataView.as_view(), name='lead-system-data-detail'),

    # Include the router URLs for the Feature ViewSets
    path('', include(router.urls)),
]