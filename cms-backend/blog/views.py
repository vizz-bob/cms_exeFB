from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404
from .models import BlogPost, BlogCategory
from .serializers import BlogPostSerializer, BlogCategorySerializer

class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogCategory.objects.all().order_by('name')
    serializer_class = BlogCategorySerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    # Set lookup_field to 'slug' so the URL router accepts strings
    lookup_field = 'slug'
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'short_description', 'body'] 

    def get_queryset(self):
        # Admin gets all posts; Public gets only published ones
        if self.request.user.is_staff:
            return BlogPost.objects.all().order_by("-created_at")
        
        queryset = BlogPost.objects.filter(published=True).order_by("-created_at")
        
        category_slug = self.request.query_params.get('category')
        if category_slug and category_slug != 'all':
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset

    # --- HYBRID LOOKUP (Fixes 404 for Public Site) ---
    def get_object(self):
        """
        Allows fetching by either ID (for Admin) or Slug (for Public).
        """
        # Get the value passed in the URL (e.g., "1" or "future-of-ai")
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)

        # 1. Try fetching by ID if it's a number (Admin Panel uses this)
        if lookup_value and lookup_value.isdigit():
            queryset = self.filter_queryset(self.get_queryset())
            # We use filter here to support the get_queryset logic (e.g. published check)
            obj = get_object_or_404(queryset, id=lookup_value)
            self.check_object_permissions(self.request, obj)
            return obj

        # 2. Otherwise, fetch by Slug (Public Site uses this)
        return super().get_object()