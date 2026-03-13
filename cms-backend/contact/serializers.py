from rest_framework import serializers
from .models import ContactMessage, ContactPage, OfficeAddress, Ticket

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        # FIX: Removed 'status' so it can be updated. Only 'created_at' is read-only.
        read_only_fields = ['created_at']

class OfficeAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeAddress
        fields = "__all__"

class ContactPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPage
        fields = "__all__"