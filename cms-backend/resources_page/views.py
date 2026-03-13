from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    ResourcesHero, SectionTitles, CaseStudy, 
    DownloadableResource, UsefulLink
)
from .serializers import (
    ResourcesHeroSerializer, SectionTitlesSerializer, CaseStudySerializer,
    DownloadableResourceSerializer, UsefulLinkSerializer
)
from blog.models import BlogPost
from blog.serializers import BlogPostSerializer

# --- 1. Public Data View (Read Only) ---
class ResourcesPageDataView(APIView):
    def get(self, request):
        # Auto-create singletons if missing
        hero, _ = ResourcesHero.objects.get_or_create(id=1)
        titles, _ = SectionTitles.objects.get_or_create(id=1)
        
        latest_blogs = BlogPost.objects.filter(published=True).order_by('-created_at')[:4]

        return Response({
            "hero": ResourcesHeroSerializer(hero).data,
            "titles": SectionTitlesSerializer(titles).data,
            "latest_blogs": BlogPostSerializer(latest_blogs, many=True).data,
            "case_studies": CaseStudySerializer(CaseStudy.objects.all(), many=True).data,
            "downloads": DownloadableResourceSerializer(DownloadableResource.objects.all(), many=True).data,
            "useful_links": UsefulLinkSerializer(UsefulLink.objects.all(), many=True).data 
        })

# --- 2. Admin CRUD ViewSets ---

class ResourcesHeroViewSet(viewsets.ModelViewSet):
    queryset = ResourcesHero.objects.all()
    serializer_class = ResourcesHeroSerializer

class SectionTitlesViewSet(viewsets.ModelViewSet):
    queryset = SectionTitles.objects.all()
    serializer_class = SectionTitlesSerializer

class CaseStudyViewSet(viewsets.ModelViewSet):
    queryset = CaseStudy.objects.all().order_by('order')
    serializer_class = CaseStudySerializer

class DownloadableResourceViewSet(viewsets.ModelViewSet):
    queryset = DownloadableResource.objects.all().order_by('order')
    serializer_class = DownloadableResourceSerializer

class UsefulLinkViewSet(viewsets.ModelViewSet):
    queryset = UsefulLink.objects.all().order_by('order')
    serializer_class = UsefulLinkSerializer