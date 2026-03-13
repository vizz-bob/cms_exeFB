from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CareersPageDataView, 
    CareersPageViewSet, 
    BenefitViewSet, 
    EmployeeTestimonialViewSet,
    JobOpeningViewSet,
    JobApplicationViewSet
)

router = DefaultRouter()

# Admin Content Routes
router.register(r'careers-content', CareersPageViewSet)
router.register(r'benefits', BenefitViewSet)
router.register(r'testimonials', EmployeeTestimonialViewSet)

# Jobs & Applications (Also registered here for Admin access)
router.register(r'jobs', JobOpeningViewSet)
router.register(r'applications', JobApplicationViewSet)

urlpatterns = [
    # Public Endpoint (Fixes 404)
    path('careers-page-data/', CareersPageDataView.as_view(), name='careers-page-data'),
    
    # Router for Admin CRUD
    path('', include(router.urls)),
]