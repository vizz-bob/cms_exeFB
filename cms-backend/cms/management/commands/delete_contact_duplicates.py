from django.core.management.base import BaseCommand
from cms.models import SiteContent
from django.db import models

class Command(BaseCommand):
    help = "Finds and deletes all duplicate SiteContent entries for the 'contact' page based on section slug."

    def handle(self, *args, **options):
        self.stdout.write('🚀 Starting duplicate clean-up for Contact Page...')
        
        # 1. Find all sections on the 'contact' page that have duplicates (count > 1)
        duplicates = (
            SiteContent.objects.filter(page='contact')
            .values('section')
            .annotate(count=models.Count('section'))
            .filter(count__gt=1)
        )
        
        if not duplicates:
            self.stdout.write(self.style.SUCCESS("✅ No duplicates found on 'contact' page. Issue may be resolved."))
            return

        self.stdout.write(self.style.WARNING(f"⚠️ Found {duplicates.count()} duplicate section slugs. Deleting extras..."))

        deleted_count = 0
        
        for item in duplicates:
            section_slug = item['section']
            
            # 2. Find all records for this specific duplicate slug
            all_duplicates = SiteContent.objects.filter(
                page='contact', 
                section=section_slug
            ).order_by('id')
            
            # 3. Keep the first (oldest) record
            original_id = all_duplicates.first().id
            
            # 4. Delete all other records
            to_delete = all_duplicates.exclude(id=original_id)
            
            count, _ = to_delete.delete()
            deleted_count += count
            
            self.stdout.write(f"   ✅ Deleted {count} duplicate(s) for section: {section_slug}")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Database clean-up complete. Total duplicates deleted: {deleted_count}. Please restart your server and try saving record ID 23 again."))