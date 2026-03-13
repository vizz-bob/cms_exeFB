from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ResourcesPageDataView,
    ResourcesHeroViewSet,
    SectionTitlesViewSet,
    CaseStudyViewSet,
    DownloadableResourceViewSet,
    UsefulLinkViewSet
)

router = DefaultRouter()
# Names match the 'resource' prop in React
router.register(r'resources-hero', ResourcesHeroViewSet)
router.register(r'section-titles', SectionTitlesViewSet)
router.register(r'case-studies', CaseStudyViewSet)
router.register(r'downloads', DownloadableResourceViewSet)
router.register(r'useful-links', UsefulLinkViewSet)

urlpatterns = [
    # Public Data
    path('resources-page-data/', ResourcesPageDataView.as_view(), name='resources-page-data'),
    
    # Admin CRUD
    path('', include(router.urls)),
]