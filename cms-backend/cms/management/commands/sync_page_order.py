from django.core.management.base import BaseCommand
from cms.models import SiteContent
from cms.sections import PAGE_SECTIONS

class Command(BaseCommand):
    help = 'Syncs the content_order field in database to match the cms/sections.py configuration'

    def handle(self, *args, **kwargs):
        self.stdout.write('🔄 Syncing Page Order with Frontend Layout...')
        
        count = 0
        
        # Iterate over every page configured in sections.py
        for page, sections in PAGE_SECTIONS.items():
            self.stdout.write(f"   📄 Processing {page.title()} Page...")
            
            # Loop through sections list (which is already in correct visual order)
            for index, section_data in enumerate(sections):
                section_slug = section_data['section']
                
                # Find the record and update its order
                try:
                    obj = SiteContent.objects.get(page=page, section=section_slug)
                    obj.content_order = index + 1 # 1-based indexing
                    obj.save()
                    count += 1
                except SiteContent.DoesNotExist:
                    # Agar record nahi mila, to ignore karo (shayad seed nahi hua)
                    pass
                except SiteContent.MultipleObjectsReturned:
                    # Duplicate safety check
                    first = SiteContent.objects.filter(page=page, section=section_slug).first()
                    first.content_order = index + 1
                    first.save()
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Successfully reordered {count} content blocks to match Frontend!'))