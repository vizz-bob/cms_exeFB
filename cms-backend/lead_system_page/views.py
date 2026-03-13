from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LSHero, LSFeature, LSBottomCTA, LSDashboard
from .serializers import LSHeroSerializer, LSFeatureSerializer, LSBottomCTASerializer, LSDashboardSerializer

# --- 1. Public Data View (Combined for Page Content) ---
class LeadSystemPageDataView(APIView):
    def get(self, request, pk=None):
        # Ensure Singletons exist
        hero, _ = LSHero.objects.get_or_create(id=1)
        dashboard, _ = LSDashboard.objects.get_or_create(id=1)
        cta, _ = LSBottomCTA.objects.get_or_create(id=1)
        
        return Response({
            "hero": LSHeroSerializer(hero).data,
            "features": LSFeatureSerializer(LSFeature.objects.all().order_by('order'), many=True).data,
            "dashboard": LSDashboardSerializer(dashboard).data,
            "cta": LSBottomCTASerializer(cta).data,
        })

    # Support both PUT and POST for updates
    def put(self, request, pk=None):
        return self.update_data(request)

    def post(self, request, pk=None):
        return self.update_data(request)

    def update_data(self, request):
        try:
            # 1. Update Hero Section
            hero, _ = LSHero.objects.get_or_create(id=1)
            hero.title = request.data.get('hero_title', hero.title)
            hero.subtitle = request.data.get('hero_subtitle', hero.subtitle)
            hero.save()

            # 2. Update Dashboard Section
            dashboard, _ = LSDashboard.objects.get_or_create(id=1)
            dashboard.placeholder_text = request.data.get('dashboard_placeholder', dashboard.placeholder_text)
            
            # Handle Image Upload (only if a new file is sent)
            if 'dashboard_image' in request.FILES:
                dashboard.image = request.FILES['dashboard_image']
            
            dashboard.save()

            # 3. Update CTA Section
            cta, _ = LSBottomCTA.objects.get_or_create(id=1)
            cta.title = request.data.get('cta_title', cta.title)
            cta.text = request.data.get('cta_text', cta.text)
            cta.save()

            # Return the updated data structure
            return self.get(request)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# --- 2. Admin ViewSets (For Features List CRUD) ---

class LSHeroViewSet(viewsets.ModelViewSet):
    queryset = LSHero.objects.all()
    serializer_class = LSHeroSerializer

class LSFeatureViewSet(viewsets.ModelViewSet):
    queryset = LSFeature.objects.all().order_by('order')
    serializer_class = LSFeatureSerializer

class LSDashboardViewSet(viewsets.ModelViewSet):
    queryset = LSDashboard.objects.all()
    serializer_class = LSDashboardSerializer

class LSBottomCTAViewSet(viewsets.ModelViewSet):
    queryset = LSBottomCTA.objects.all()
    serializer_class = LSBottomCTASerializer