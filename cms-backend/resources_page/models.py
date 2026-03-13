from django.db import models
from django.core.validators import FileExtensionValidator 

class ResourcesHero(models.Model):
    title = models.CharField(max_length=255, default="Knowledge Hub")
    subtitle = models.TextField(default="Expert insights, whitepapers, and success stories to guide your financial strategy.")
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Resources Hero Content"

class SectionTitles(models.Model):
    case_studies_title = models.CharField(max_length=255, default="Client Success Stories")
    downloads_title = models.CharField(max_length=255, default="Essential Downloads")

    class Meta:
        verbose_name = "Section Titles"
        verbose_name_plural = "Section Titles"

    def __str__(self):
        return "Section Titles"

class CaseStudy(models.Model):
    title = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    summary = models.TextField()
    result_stat = models.CharField(max_length=100, help_text="e.g. '300% Growth'")
    pdf_file = models.FileField(upload_to="casestudies/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class DownloadableResource(models.Model):
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=50, choices=[
        ('E-Book', 'E-Book'), 
        ('Whitepaper', 'Whitepaper'), 
        ('Guide', 'Guide'), 
        ('Report', 'Report'),
        ('Presentation', 'Presentation'),
        ('Dataset', 'Dataset')
    ])
    description = models.TextField()
    
    # --- FILE UPLOAD SUPPORT ---
    file = models.FileField(
        upload_to="resources/", 
        blank=True, 
        null=True,
        help_text="Upload your document here (PDF, Excel, CSV, PPT, Word, etc.)",
        validators=[FileExtensionValidator(allowed_extensions=[
            'pdf', 'csv', 'xlsx', 'xls', 'ppt', 'pptx', 'doc', 'docx', 'txt', 'zip'
        ])]
    )
    
    # --- EXTERNAL LINK SUPPORT ---
    external_link = models.URLField(
        blank=True, 
        null=True, 
        help_text="Optional: Link to external article/resource if no file is uploaded"
    )
    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    
class UsefulLink(models.Model):
    title = models.CharField(max_length=255, help_text="e.g. 'ICAI Official Website'")
    url = models.URLField(help_text="External URL (e.g. https://www.icai.org/)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Useful Link"
        verbose_name_plural = "Useful Links"

    def __str__(self):
        return self.title