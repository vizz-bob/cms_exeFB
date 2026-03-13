from rest_framework import serializers
from .models import (
    HomePageContent, TrustedClient, 
    ProcessStep, Testimonial, FAQ
)

class HomePageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageContent
        fields = '__all__'

class TrustedClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustedClient
        fields = '__all__'

class ProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'