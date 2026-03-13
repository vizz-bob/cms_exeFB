from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SiteContentViewSet, get_section_choices

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'sitecontent', SiteContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sections/<str:page>/', get_section_choices, name='get_section_choices'),
]