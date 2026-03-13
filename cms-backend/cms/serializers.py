from rest_framework import serializers
from .models import SiteContent, CaseStudy, Resource, Service, ServiceSubService, Page
import json

class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = ['id', 'page', 'section', 'title', 'content', 'image', 'updated_at']

class CaseStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

# --- SERVICE SERIALIZERS ---

class ServiceSubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSubService
        fields = ['id', 'title', 'description', 'order']

class ServiceSerializer(serializers.ModelSerializer):
    # 1. Read-only nested data for the frontend to display
    sub_services = ServiceSubServiceSerializer(many=True, read_only=True)
    
    # 2. Write-only field to accept the JSON string from React FormData
    sub_services_content = serializers.CharField(write_only=True, required=False)

    # 3. CRITICAL FIX: Explicitly mark these as optional to prevent 400 Errors
    #    This allows the frontend to send "nothing" for these fields without crashing.
    image = serializers.ImageField(required=False, allow_null=True)
    icon = serializers.CharField(required=False, allow_blank=True)
    slug = serializers.CharField(required=False, allow_blank=True)
    short_description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Service
        fields = '__all__'

    def create(self, validated_data):
        sub_services_json = validated_data.pop('sub_services_content', None)
        
        # If slug is empty string, remove it so model's auto-slug generation works (if applicable)
        if 'slug' in validated_data and not validated_data['slug']:
            validated_data.pop('slug')

        service = Service.objects.create(**validated_data)

        if sub_services_json:
            self._save_sub_services(service, sub_services_json)

        return service

    def update(self, instance, validated_data):
        sub_services_json = validated_data.pop('sub_services_content', None)

        # Handle slug specifically to allow blank -> auto-generate logic if your model supports it
        if 'slug' in validated_data and not validated_data['slug']:
            validated_data.pop('slug')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if sub_services_json:
            # Replace strategy: Delete old, create new
            instance.sub_services.all().delete()
            self._save_sub_services(instance, sub_services_json)

        return instance

    def _save_sub_services(self, service, json_data):
        try:
            items = json.loads(json_data)
            sub_service_objects = []
            for index, item in enumerate(items):
                sub_service_objects.append(
                    ServiceSubService(
                        service=service,
                        title=item.get('title', ''),
                        description=item.get('description', ''),
                        order=index
                    )
                )
            ServiceSubService.objects.bulk_create(sub_service_objects)
        except json.JSONDecodeError:
            pass # Ignore invalid JSON
        except Exception as e:
            print(f"Error saving sub-services: {e}")

# --- PAGE SERIALIZER ---
class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'