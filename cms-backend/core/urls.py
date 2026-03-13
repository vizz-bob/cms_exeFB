from django.urls import path
from . import views
from .views import (
    RegisterView, 
    CustomLoginView, 
    UserProfileView,
    SystemStatusView, 
    SetupAdminView
)

urlpatterns = [
    path('', views.home, name='home'),
    
    # --- Authentication APIs ---
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', CustomLoginView.as_view(), name='login'),
    
    # --- Profile API ---
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

    # --- System Setup APIs (New) ---
    path('api/system-status/', SystemStatusView.as_view(), name='system-status'),
    path('api/setup-admin/', SetupAdminView.as_view(), name='setup-admin'),
]