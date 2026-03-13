from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StakeholderViewSet, SolutionsPageDataView, SolutionDetailView

router = DefaultRouter()
router.register(r'stakeholders', StakeholderViewSet)

urlpatterns = [
    # Main Solutions Page Data
    path('solutions-page-data/', SolutionsPageDataView.as_view(), name='solutions-page-data'),
    
    # Detail Page Data (e.g., /api/solutions/for-clients/)
    path('solutions/<slug:slug>/', SolutionDetailView.as_view(), name='solution-detail'),
] + router.urls