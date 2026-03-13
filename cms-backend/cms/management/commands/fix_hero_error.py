from django.core.management.base import BaseCommand
from cms.models import SiteContent

class Command(BaseCommand):
    help = 'Fixes the Hero Image section naming conflict for ID 273'

    def handle(self, *args, **kwargs):
        target_id = 273  # Jo ID error de rahi hai
        
        try:
            # 1. Fetch the problematic record
            record = SiteContent.objects.get(id=target_id)
            
            self.stdout.write(f"🔍 Found Record {target_id}: {record}")
            self.stdout.write(f"   Current Name: '{record.section_name}' | Slug: '{record.section}'")

            # 2. Rename it to the correct unique name
            new_name = "Hero Image"
            new_slug = "hero_image"
            
            # Check if 'hero_image' already exists on another ID to avoid collision
            conflict = SiteContent.objects.filter(page='home', section=new_slug).exclude(id=target_id).first()
            
            if conflict:
                self.stdout.write(self.style.WARNING(f"⚠️ Conflict found! ID {conflict.id} already has name '{new_name}'. Deleting it to clear path..."))
                conflict.delete()

            # 3. Apply changes
            record.section_name = new_name
            record.section = new_slug
            record.save()

            self.stdout.write(self.style.SUCCESS(f"✅ Fixed! Record {target_id} renamed to '{new_name}'. You can now edit it in Admin."))

        except SiteContent.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Record {target_id} not found. Are you sure that is the correct ID?"))

        # 4. Optional: Clean up generic 'Hero' duplicates if any remain
        duplicates = SiteContent.objects.filter(page='home', section='hero').exclude(id=target_id)
        if duplicates.exists():
            count = duplicates.count()
            duplicates.delete()
            self.stdout.write(self.style.WARNING(f"🧹 Cleaned up {count} other duplicate 'Hero' entries."))