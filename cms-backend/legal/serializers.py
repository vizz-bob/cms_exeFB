from rest_framework import serializers
from .models import LegalPage, LegalPageSection

class LegalPageSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalPageSection
        fields = ['heading', 'content', 'order']

class LegalPageSerializer(serializers.ModelSerializer):
    # Sections ko nested data ki tarah bhejein
    sections = LegalPageSectionSerializer(many=True, read_only=True)

    class Meta:
        model = LegalPage
        fields = ['id', 'title', 'slug', 'description', 'last_updated', 'sections']