from django.db import models

class HomePageContent(models.Model):
    """
    Singleton model to manage all text content, titles, and single sections on the Home Page.
    """
    # --- 1. HERO SECTION ---
    hero_title = models.CharField(max_length=255, default="Next-Gen Financial Intelligence")
    hero_subtitle = models.TextField(default="Automate audits, tax compliance, and forecasting with AI precision.")
    # Removed hero_image as per frontend update
    hero_cta_text = models.CharField(max_length=50, default="Start Free Trial")
    hero_cta_link = models.CharField(max_length=200, default="/contact", blank=True)
    hero_sec_btn_text = models.CharField(max_length=50, default="How It Works", blank=True)

    # --- 2. AI RECOMMENDATION SECTION (New) ---
    ai_title = models.CharField(max_length=255, default="Not sure where to start?", blank=True)
    ai_subtitle = models.CharField(max_length=255, default="Let our AI-powered selector guide you.", blank=True)

    # --- 3. SECTION HEADERS ---
    process_title = models.CharField(max_length=255, default="How It Works", blank=True)
    process_subtitle = models.TextField(default="Seamless integration in 3 simple steps.", blank=True)

    # Renamed from features_title to match frontend 'services_title'
    services_title = models.CharField(max_length=255, default="Our Key Services", blank=True)
    
    clients_title = models.CharField(max_length=255, default="Trusted by Industry Leaders", blank=True)
    reviews_title = models.CharField(max_length=255, default="Client Success Stories", blank=True)
    stories_title = models.CharField(max_length=255, default="Success Stories", blank=True)
    faq_title = models.CharField(max_length=255, default="Frequently Asked Questions", blank=True)

    # --- 4. BOTTOM CTA SECTION (Consolidated 3 Buttons) ---
    cta_title = models.CharField(max_length=255, default="Ready to Transform?")
    cta_text = models.TextField(default="Join 500+ companies streamlining their finance today.")
    
    # Button 1 (Left)
    quick_link_1_text = models.CharField(max_length=50, default="Sign Up", blank=True)
    quick_link_1_link = models.CharField(max_length=200, default="/contact", blank=True)
    
    # Button 2 (Center)
    quick_link_2_text = models.CharField(max_length=50, default="Explore Services", blank=True)
    quick_link_2_link = models.CharField(max_length=200, default="/services", blank=True)
    
    # Button 3 (Right)
    quick_link_3_text = models.CharField(max_length=50, default="Join as Professional", blank=True)
    quick_link_3_link = models.CharField(max_length=200, default="/careers", blank=True)

    def __str__(self):
        return "Home Page Main Content"

    class Meta:
        verbose_name = "Home Page Setup"
        verbose_name_plural = "Home Page Setup"


# --- LIST MODELS (Multiple Items) ---

class TrustedClient(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="clients/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class ProcessStep(models.Model):
    step_number = models.CharField(max_length=10, default="01")
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default="Settings")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.step_number} - {self.title}"

class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    quote = models.TextField()
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.author_name

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"

    def __str__(self):
        return self.question