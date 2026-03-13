from rest_framework import serializers
from .models import BlogPost, BlogCategory

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug']

class BlogPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    
    # Read Only: Show full category details
    category = BlogCategorySerializer(read_only=True)
    
    # Write Only: Accept category ID from Admin
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(), 
        source='category', 
        write_only=True, 
        required=False, 
        allow_null=True
    )

    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "slug", "short_description", "body", 
            "image", "published", "created_at", 
            "category", "category_id"
        ]
        # FIX: Make slug read-only so the API doesn't demand it
        read_only_fields = ['slug', 'created_at']