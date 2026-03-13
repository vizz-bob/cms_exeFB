from django.db import models

class LSHero(models.Model):
    title = models.CharField(max_length=255, default="Lead Management System")
    subtitle = models.TextField(default="Track, Manage, and Convert leads with AI precision.")
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Lead System Hero"

class LSFeature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default="Target", help_text="Lucide Icon Name")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Feature Card"
        verbose_name_plural = "Feature Cards"

    def __str__(self):
        return self.title

class LSDashboard(models.Model):
    image = models.ImageField(upload_to="lead_system/", blank=True, null=True, help_text="Upload the Dashboard Preview Image here")
    placeholder_text = models.CharField(max_length=255, default="Dashboard Preview", help_text="Alt text for the image")

    class Meta:
        verbose_name = "Dashboard Preview"
        verbose_name_plural = "Dashboard Preview"

    def __str__(self):
        return "Dashboard Image Section"

class LSBottomCTA(models.Model):
    title = models.CharField(max_length=255, default="Ready to Streamline?")
    text = models.TextField(default="Join the platform that powers high-growth teams.")
    button_text = models.CharField(max_length=50, default="Get Started")

    class Meta:
        verbose_name = "Bottom CTA"
        verbose_name_plural = "Bottom CTA"

    def __str__(self):
        return "Lead System CTA"