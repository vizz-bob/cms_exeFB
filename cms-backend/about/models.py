from django.db import models

class AboutPage(models.Model):
    # --- 1. Hero Section ---
    hero_title = models.CharField(max_length=255, default="About XpertAI Global")
    hero_subtitle = models.TextField(default="Pioneering the future of financial intelligence.")
    hero_image = models.ImageField(upload_to="about/", blank=True, null=True)

    # --- 2. Mission, Vision, Values ---
    mission_title = models.CharField(max_length=255, default="Our Mission")
    mission_text = models.TextField(default="To empower businesses with AI-driven financial clarity.")
    
    vision_title = models.CharField(max_length=255, default="Our Vision")
    vision_text = models.TextField(default="A world where finance is automated, accurate, and strategic.")
    
    values_title = models.CharField(max_length=255, default="Our Values")
    values_text = models.TextField(default="Integrity, Innovation, and Impact.")

    # --- 3. Our Story ---
    story_title = models.CharField(max_length=255, default="Our Story", blank=True)
    story_text = models.TextField(blank=True, help_text="How we started...")
    story_image = models.ImageField(upload_to="about/", blank=True, null=True)

    # --- 4. Global Presence ---
    global_title = models.CharField(max_length=255, default="Global Presence", blank=True)
    global_stats = models.CharField(max_length=255, default="Active in 15+ Countries", blank=True)
    
    # --- 5. Awards & Recognition (Ye field missing tha isliye error aya) ---
    awards_title = models.CharField(max_length=255, default="Awards & Recognition", blank=True)

    # --- 6. Sustainability / CSR ---
    csr_title = models.CharField(max_length=255, default="Sustainability", blank=True)
    csr_text = models.TextField(blank=True, help_text="Our commitment to the planet.")

    # --- 7. CTA (Bottom) ---
    cta_title = models.CharField(max_length=255, default="Join Our Journey")
    cta_text = models.TextField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Page Setup"
        verbose_name_plural = "About Page Setup"

    def __str__(self):
        return "About Page Content"

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="team/", blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Award(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon_image = models.ImageField(upload_to="awards/", blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

class TechStack(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default="Cpu", help_text="Lucide Icon Name (e.g. Cpu, Link, Bot)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Technology Stack"
        verbose_name_plural = "Technology Stack"

    def __str__(self):
        return self.title