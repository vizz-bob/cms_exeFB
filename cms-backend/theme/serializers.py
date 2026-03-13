from rest_framework import serializers
from .models import ChatbotFlowStep

class ChatbotFlowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotFlowStep
        fields = '__all__'