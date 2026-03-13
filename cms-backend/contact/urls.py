# contact/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContactViewSet, 
    ContactPageDataView, 
    ContactPageViewSet, 
    OfficeAddressViewSet, 
    ContactMessageViewSet, 
    TicketViewSet
)

router = DefaultRouter()

# Admin Endpoints
router.register(r'contact-content', ContactPageViewSet)
router.register(r'office-addresses', OfficeAddressViewSet)
router.register(r'messages', ContactMessageViewSet)

# FIX: Add basename='ticket' because TicketViewSet uses get_queryset()
router.register(r'tickets', TicketViewSet, basename='ticket') 

# Public Endpoint
router.register(r'', ContactViewSet, basename="public-contact")

urlpatterns = [
    path('page-data/', ContactPageDataView.as_view(), name='contact-page-data'),
    path('', include(router.urls)),
]