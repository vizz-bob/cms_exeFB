from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, BlogCategoryViewSet # <-- Import Naya ViewSet

router = DefaultRouter()
router.register(r"blogs", BlogPostViewSet, basename="blog")
router.register(r"blog-categories", BlogCategoryViewSet, basename="blog-category") # <-- NEW ROUTE ADDED

urlpatterns = router.urls