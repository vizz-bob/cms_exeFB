from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField(help_text="Query/Message from the user")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    description = models.TextField(help_text="Detailed explanation of the issue")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.subject}"

class ContactPage(models.Model):
    """
    Singleton model for Contact Page static content & Map.
    """
    # --- Hero Section ---
    hero_title = models.CharField(max_length=255, default="Get in Touch")
    hero_subtitle = models.TextField(default="We'd love to hear from you. Reach out to us for any queries.")
    
    # --- Form Configuration ---
    form_title = models.CharField(max_length=255, default="Send us a Message")
    form_button_text = models.CharField(max_length=50, default="Request Consultation")
    
    # Form Labels (Editable by Admin)
    form_name_label = models.CharField(max_length=100, default="Name")
    form_company_label = models.CharField(max_length=100, default="Company")
    form_email_label = models.CharField(max_length=100, default="Email")
    form_phone_label = models.CharField(max_length=100, default="Phone")
    form_service_label = models.CharField(max_length=100, default="I am interested in...")
    form_timeline_label = models.CharField(max_length=100, default="Timeline")
    form_message_label = models.CharField(max_length=100, default="Message")

    # Functional Settings
    is_sub_service_multiselect = models.BooleanField(
        default=True, 
        help_text="Uncheck to force users to select only ONE sub-service."
    )
    
    # --- Map Integration ---
    map_embed_url = models.TextField(
        help_text="Paste the Google Maps Embed iframe 'src' URL here (starts with https://www.google.com/maps/embed...)",
        default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3770.792576390356!2d72.87765631490116!3d19.07609098708786!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c6306644edc1%3A0x5da4ed8f8d648c69!2sMumbai%2C%20Maharashtra!5e0!3m2!1sen!2sin!4v1625567890123!5m2!1sen!2sin"
    )
    
    # --- Support Section ---
    support_title = models.CharField(max_length=255, default="Support & Assistance")
    support_text = models.TextField(default="Need help? Choose the right channel for a quick resolution.")

    def __str__(self):
        return "Contact Page Setup"

    class Meta:
        verbose_name = "Contact Page Setup"
        verbose_name_plural = "Contact Page Setup"

class OfficeAddress(models.Model):
    title = models.CharField(max_length=100, help_text="e.g. Corporate Office, Branch Office")
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title