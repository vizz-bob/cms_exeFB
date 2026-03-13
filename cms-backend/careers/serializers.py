from rest_framework import serializers
from .models import CareersPage, Benefit, JobOpening, JobApplication, EmployeeTestimonial

class CareersPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareersPage
        fields = '__all__'

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'

class EmployeeTestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTestimonial
        fields = '__all__'

class JobOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    # Ensure links are optional in serializer validation
    resume_link = serializers.URLField(required=False, allow_blank=True)
    linkedin_url = serializers.URLField(required=False, allow_blank=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'