from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, ClientProfile, ProfessionalProfile, TrainingProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        if hasattr(user, 'profile'):
            profile = user.profile
            profile.role = role
            profile.save()

        if role == 'client':
            ClientProfile.objects.create(user=user)
        elif role in ['professional', 'freelancer']:
            is_agency = True if role == 'professional' else False
            ProfessionalProfile.objects.create(user=user, is_agency=is_agency)
        elif role == 'trainer':
            TrainingProfile.objects.create(user=user)
        
        return user

# --- NEW: Profile Serializer ---
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = UserProfile
        fields = [
            'username', 'email', 'first_name', 'last_name', 'phone', 'address', 'profile_image', 'role', 
            'password', 'confirm_password',
            'job_title', 'bio', 'linkedin_url', 'twitter_url', 'website_url',
            'leads_notification_email' # <-- Added
        ]
        read_only_fields = ['role']

    def validate(self, data):
        if 'password' in data and data['password'] != data.get('confirm_password'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        if 'user' in data and 'username' in data['user']:
            new_username = data['user']['username']
            if User.objects.filter(username=new_username).exclude(pk=self.instance.user.pk).exists():
                raise serializers.ValidationError({"username": "This username is already taken."})
        
        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)

        user = instance.user
        
        if 'username' in user_data: user.username = user_data['username']
        if 'first_name' in user_data: user.first_name = user_data['first_name']
        if 'last_name' in user_data: user.last_name = user_data['last_name']
        if 'email' in user_data: user.email = user_data['email']
        
        if password:
            user.set_password(password)
        
        user.save()
        return super().update(instance, validated_data)