from rest_framework import serializers
from .models import LSHero, LSFeature, LSBottomCTA, LSDashboard

class LSHeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = LSHero
        fields = '__all__'

class LSFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LSFeature
        fields = '__all__'

class LSDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LSDashboard
        fields = '__all__'

class LSBottomCTASerializer(serializers.ModelSerializer):
    class Meta:
        model = LSBottomCTA
        fields = '__all__'