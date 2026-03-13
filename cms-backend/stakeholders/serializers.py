from rest_framework import serializers
from .models import SolutionsPage, Stakeholder

class SolutionsPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionsPage
        fields = '__all__'

class StakeholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakeholder
        fields = '__all__'