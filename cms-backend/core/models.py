from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- 1. EXISTING MODELS ---
class ExampleModel(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self): return self.name

class Theme(models.Model):
    primary_color = models.CharField(max_length=7, default='#000000')
    secondary_color = models.CharField(max_length=7, default='#FFFFFF')
    def __str__(self): return "Website Theme"

# --- 2. UPDATED USER SYSTEM ---

USER_ROLES = (
    ('admin', 'Admin'),
    ('client', 'Client'),
    ('professional', 'Professional/Agency'),
    ('freelancer', 'Freelancer'),
    ('trainer', 'Training Institute/Trainer'),
)

class UserProfile(models.Model):
    # FIX: primary_key=True keeps the user ID as profile ID
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    
    # Role Selection
    role = models.CharField(max_length=20, choices=USER_ROLES, default='client')
    
    # Common Fields
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # Verification Status
    is_verified = models.BooleanField(default=False)

    # --- NEW FIELDS (Bio, Job, Social) ---
    job_title = models.CharField(max_length=100, blank=True, help_text="e.g. Senior Auditor")
    bio = models.TextField(blank=True, help_text="Short 'About Me' section")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn Profile URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter/X Profile URL")
    website_url = models.URLField(blank=True, help_text="Personal Portfolio or Company Website")
    
    # --- ADMIN SETTINGS ---
    # Field to set where lead notifications should be sent
    leads_notification_email = models.EmailField(blank=True, null=True, help_text="Email to receive lead notifications")

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

# --- SPECIFIC PROFILES ---

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    company_name = models.CharField(max_length=255, blank=True)
    gst_number = models.CharField(max_length=50, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Client: {self.company_name or self.user.username}"

class ProfessionalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional_profile')
    skills = models.TextField(help_text="Comma separated skills (e.g. Audit, GST, Python)")
    experience_years = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    is_agency = models.BooleanField(default=False, help_text="Check if this is an Agency")
    
    def __str__(self):
        return f"Pro: {self.user.username}"

class TrainingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='training_profile')
    institute_name = models.CharField(max_length=255)
    courses_offered = models.TextField(help_text="List of courses")
    
    def __str__(self):
        return f"Trainer: {self.institute_name}"

# --- SIGNALS ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)