from rest_framework import serializers
from .models import AboutPage, TeamMember, Award, TechStack

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'

class TechStackSerializer(serializers.ModelSerializer): # <--- New Serializer
    class Meta:
        model = TechStack
        fields = '__all__'

class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage
        fields = '__all__'