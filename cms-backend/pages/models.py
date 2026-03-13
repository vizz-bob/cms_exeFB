from django.db import models

class PageContent(models.Model):
    """
    A model to store editable content for a single page.
    """
    # A unique identifier for the page, e.g., 'about-us', 'contact-info'
    # This helps the frontend know which content to fetch.
    slug = models.SlugField(unique=True, primary_key=True, help_text="A unique name for the page, used to identify it.")
    
    title = models.CharField(max_length=200, help_text="The main title of the page.")
    
    # Use TextField for large blocks of text. It can store HTML.
    content = models.TextField(blank=True, help_text="The main content of the page. Can include HTML.")

    # This helps identify the object in the admin list.
    def __str__(self):
        return self.title
