from django.db import models
from django.utils.text import slugify

class SolutionsPage(models.Model):
    """
    Singleton model for the Solutions Page Hero and CTA sections.
    """
    hero_title = models.CharField(max_length=200, default="Our Solutions")
    hero_subtitle = models.TextField(default="Tailored ecosystems for every stakeholder in the financial world.")
    
    cta_title = models.CharField(max_length=200, default="Ready to join the ecosystem?")
    cta_text = models.TextField(default="Whether you are a client looking for experts or a professional seeking work, XpertAI has a place for you.")
    
    # Optional button fields if needed in future
    cta_btn_primary = models.CharField(max_length=50, default="Sign Up Now")
    cta_btn_secondary = models.CharField(max_length=50, default="Contact Sales")
    
    class Meta:
        verbose_name = "Solutions Page Content"
        verbose_name_plural = "Solutions Page Content"

    def __str__(self):
        return "Solutions Page Content"

class Stakeholder(models.Model):
    """
    Represents an individual Solution/Stakeholder card.
    """
    title = models.CharField(max_length=200)
    
    # Allow null temporarily for migrations, auto-generated on save
    slug = models.SlugField(
        unique=True, 
        blank=True, 
        null=True, 
        help_text="Unique URL identifier (auto-generated from title)"
    )
    
    description = models.TextField(help_text="Short summary shown on the card")
    long_description = models.TextField(blank=True, help_text="Detailed text for the individual solution page")
    
    icon_name = models.CharField(max_length=50, default="Layers", help_text="Lucide Icon Name (e.g. Layers, Briefcase)")
    image = models.ImageField(upload_to="stakeholders/", blank=True, null=True)
    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Solution Card"
        verbose_name_plural = "Solution Cards"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)