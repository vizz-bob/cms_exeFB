from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LegalPageViewSet, LegalPageSectionViewSet

router = DefaultRouter()
router.register(r'pages', LegalPageViewSet, basename='legal-page')
router.register(r'sections', LegalPageSectionViewSet, basename='legal-section')

urlpatterns = [
    path('', include(router.urls)),
]