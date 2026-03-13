from django.db import models

class SiteBranding(models.Model):
    site_title = models.CharField(max_length=255, default="XpertAI Global")
    logo = models.ImageField(upload_to="branding/logos/", blank=True, null=True)
    favicon = models.ImageField(upload_to="branding/favicons/", blank=True, null=True)
    
    # Announcement Bar
    show_announcement = models.BooleanField(default=False)
    announcement_text = models.CharField(max_length=500, blank=True, default="Welcome to our new website!")
    announcement_link = models.CharField(max_length=500, blank=True, default="#")
    
    # --- 🆕 HEADER NAVIGATION LABELS (Menu Names) ---
    nav_about_label = models.CharField(max_length=50, default="About")
    nav_services_label = models.CharField(max_length=50, default="Services")
    nav_solutions_label = models.CharField(max_length=50, default="Solutions")
    nav_careers_label = models.CharField(max_length=50, default="Careers")
    nav_resources_label = models.CharField(max_length=50, default="Resources")
    nav_cta_label = models.CharField(max_length=50, default="Get Started") # Button ka text
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            SiteBranding.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_title