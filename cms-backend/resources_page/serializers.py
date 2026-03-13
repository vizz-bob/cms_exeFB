from rest_framework import serializers
from .models import (
    ResourcesHero, SectionTitles, CaseStudy, 
    DownloadableResource, UsefulLink
)

class ResourcesHeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourcesHero
        fields = '__all__'

class SectionTitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionTitles
        fields = '__all__'

class CaseStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = '__all__'

class DownloadableResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadableResource
        fields = '__all__'

class UsefulLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsefulLink
        fields = '__all__'