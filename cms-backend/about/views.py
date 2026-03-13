from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AboutPage, TeamMember, Award, TechStack
from .serializers import (
    AboutPageSerializer, TeamMemberSerializer, 
    AwardSerializer, TechStackSerializer
)

# --- 1. Public API (Aggregated Data for Frontend) ---
class AboutPageDataView(APIView):
    def get(self, request):
        # FIX: Use get_or_create to ensure content always exists (prevents frontend crash)
        content, created = AboutPage.objects.get_or_create(id=1)
        
        team_members = TeamMember.objects.all()
        awards = Award.objects.all()
        tech_stack = TechStack.objects.all()

        return Response({
            "content": AboutPageSerializer(content).data,
            "team": TeamMemberSerializer(team_members, many=True).data,
            "awards": AwardSerializer(awards, many=True).data,
            "tech_stack": TechStackSerializer(tech_stack, many=True).data
        })

# --- 2. Admin CRUD ViewSets (For Editing) ---

class AboutPageViewSet(viewsets.ModelViewSet):
    """
    For updating the Singleton About Content (Hero, Mission, Stories, etc.)
    """
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer

class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

class TechStackViewSet(viewsets.ModelViewSet):
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer