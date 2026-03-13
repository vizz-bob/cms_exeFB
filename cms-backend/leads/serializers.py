from rest_framework import serializers
from .models import Lead, NewsletterSubscriber, LeadShareHistory, EmailTemplate

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'subscribed_at', 'is_active']
        read_only_fields = ['subscribed_at']

# --- Share History Serializer ---
class LeadShareHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadShareHistory
        fields = ['id', 'recipient_name', 'recipient_phone', 'shared_at', 'platform']

# --- NEW: Email Template Serializer ---
class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'