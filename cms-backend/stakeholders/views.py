from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import SolutionsPage, Stakeholder
from .serializers import SolutionsPageSerializer, StakeholderSerializer

# --- 1. Public Data View (Combined) ---
class SolutionsPageDataView(APIView):
    def get(self, request):
        # Ensure content exists
        content, _ = SolutionsPage.objects.get_or_create(id=1)
        solutions = Stakeholder.objects.all().order_by('order')
        
        return Response({
            "content": SolutionsPageSerializer(content).data,
            "solutions": StakeholderSerializer(solutions, many=True).data
        })

# --- 2. Admin & Detail ViewSets ---

class SolutionsPageViewSet(viewsets.ModelViewSet):
    """
    API for editing the Hero and CTA text.
    """
    queryset = SolutionsPage.objects.all()
    serializer_class = SolutionsPageSerializer

class StakeholderViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Solutions/Stakeholders.
    Supports lookup by ID (Admin) and Slug (Public).
    """
    queryset = Stakeholder.objects.all().order_by('order')
    serializer_class = StakeholderSerializer
    lookup_field = 'slug' # Default for public URLs

    def get_object(self):
        """
        Hybrid Lookup:
        - If URL param is an Integer (e.g. '1'), fetch by ID (for Admin Editing).
        - If URL param is a String (e.g. 'corporate-clients'), fetch by Slug (for Public View).
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)

        # 1. Try fetching by ID first (if it's a number)
        if lookup_value and lookup_value.isdigit():
            queryset = self.filter_queryset(self.get_queryset())
            obj = get_object_or_404(queryset, id=lookup_value)
            self.check_object_permissions(self.request, obj)
            return obj

        # 2. Otherwise, fetch by Slug
        return super().get_object()

# --- 3. Dedicated Detail View (Optional, but kept for compatibility) ---
class SolutionDetailView(generics.RetrieveAPIView):
    queryset = Stakeholder.objects.all()
    serializer_class = StakeholderSerializer
    lookup_field = 'slug'