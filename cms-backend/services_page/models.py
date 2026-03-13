from django.db import models

class ServiceHero(models.Model):
    title = models.CharField(max_length=255, default="Our Expertise")
    subtitle = models.TextField(default="Comprehensive financial solutions tailored for your business growth.")
    image = models.ImageField(upload_to="services_page/", blank=True, null=True)
    cta_text = models.CharField(max_length=50, default="Explore Services")

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Service Hero Content"

class ServiceProcess(models.Model):
    step_number = models.CharField(max_length=10, default="01")
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default="Settings", help_text="Lucide Icon Name")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class ServiceFeature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default="CheckCircle")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class ServiceTestimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    quote = models.TextField()
    image = models.ImageField(upload_to="services_page/testimonials/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class ServiceFAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"

    def __str__(self):
        return self.question

class ServiceCTA(models.Model):
    title = models.CharField(max_length=255, default="Ready to optimize your finance?")
    text = models.TextField(default="Book a consultation with our experts today.")
    button_text = models.CharField(max_length=50, default="Get a Custom Quote")

    class Meta:
        verbose_name = "Bottom CTA"
        verbose_name_plural = "Bottom CTA"

    def __str__(self):
        return "Service Bottom CTA"