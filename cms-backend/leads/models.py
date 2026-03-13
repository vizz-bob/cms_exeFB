from django.db import models
from django.conf import settings  # Required for AUTH_USER_MODEL

class Lead(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    
    # --- Service Fields ---
    service = models.CharField(max_length=200, blank=True, help_text="Main Service Category")
    sub_services = models.TextField(blank=True, help_text="Comma-separated list of selected sub-services")
    timeline = models.CharField(max_length=100, blank=True, help_text="When is the service required?")
    # ------------------------------

    message = models.TextField(blank=True)
    source = models.CharField(max_length=100, blank=True, default="website")
    
    # --- UPDATED STATUS CHOICES ---
    STATUS_CHOICES = [
        ('new', 'New'),
        ('forwarded', 'Forwarded'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
        ('spam', 'Spam'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Shows Name, Service, and Date in Admin dropdowns
        return f"{self.name} ({self.service}) - {self.created_at.strftime('%Y-%m-%d')}"

# --- PROXY MODELS ---

class ChatbotLeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(source='chatbot')

class ChatbotLead(Lead):
    objects = ChatbotLeadManager()
    class Meta:
        proxy = True
        verbose_name = 'Chatbot Lead'
        verbose_name_plural = 'Chatbot Leads'

class WebsiteLeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(source='website')

class WebsiteLead(Lead):
    objects = WebsiteLeadManager()
    class Meta:
        proxy = True
        verbose_name = 'Website Lead'
        verbose_name_plural = 'Website Leads'

# --- SUBSCRIBERS ---

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

# --- SHARE HISTORY MODEL ---
class LeadShareHistory(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='share_history')
    recipient_name = models.CharField(max_length=255, help_text="Name of the person receiving the lead")
    recipient_phone = models.CharField(max_length=20, help_text="WhatsApp Number of the recipient")
    
    shared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    shared_at = models.DateTimeField(auto_now_add=True)
    platform = models.CharField(max_length=20, default='whatsapp', choices=[('whatsapp', 'WhatsApp'), ('email', 'Email')])

    class Meta:
        ordering = ['-shared_at']
        verbose_name = "Lead Share Log"
        verbose_name_plural = "Lead Share Logs"

    def __str__(self):
        return f"Shared with {self.recipient_name} on {self.shared_at.strftime('%d %b, %H:%M')}"

# --- EMAIL TEMPLATE MODEL ---
class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, help_text="Internal name for the template (e.g., 'Welcome Email')")
    subject = models.CharField(max_length=255)
    body = models.TextField(help_text="The content of the email.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name