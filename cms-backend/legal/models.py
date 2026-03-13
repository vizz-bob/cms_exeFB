from django.db import models

class LegalPage(models.Model):
    title = models.CharField(max_length=200, help_text="Page Title (e.g. Privacy Policy)")
    slug = models.SlugField(unique=True, help_text="URL identifier (e.g. privacy-policy)")
    description = models.TextField(blank=True, help_text="Short Intro Text (Optional)")
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class LegalPageSection(models.Model):
    legal_page = models.ForeignKey(LegalPage, related_name='sections', on_delete=models.CASCADE)
    heading = models.CharField(max_length=255, help_text="Section Heading (e.g. '1. Introduction')")
    content = models.TextField(help_text="Is heading ka content yahan likhein.")
    order = models.PositiveIntegerField(default=0, help_text="Sequence number (1, 2, 3...)")

    class Meta:
        ordering = ['order']
        verbose_name = "Legal Page Section"
        verbose_name_plural = "Legal Page Sections"

    def __str__(self):
        return self.heading