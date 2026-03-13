from rest_framework import serializers
from .models import (
    ServiceHero, ServiceProcess, ServiceFeature, 
    ServiceTestimonial, ServiceFAQ, ServiceCTA
)

class ServiceHeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceHero
        fields = '__all__'

class ServiceProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProcess
        fields = '__all__'

class ServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeature
        fields = '__all__'

class ServiceTestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTestimonial
        fields = '__all__'

class ServiceFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFAQ
        fields = '__all__'

class ServiceCTASerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCTA
        fields = '__all__'