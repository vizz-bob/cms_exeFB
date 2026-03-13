from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SiteBrandingViewSet

router = DefaultRouter()
router.register(r'config', SiteBrandingViewSet, basename='branding')

urlpatterns = [
    path('', include(router.urls)),
]