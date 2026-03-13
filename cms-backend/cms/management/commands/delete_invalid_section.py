from django.core.management.base import BaseCommand
from cms.models import SiteContent

class Command(BaseCommand):
    help = 'Deletes the invalid section "a1" for the "home" page'

    def handle(self, *args, **options):
        try:
            item = SiteContent.objects.get(page='home', section='a1')
            item.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted invalid section "a1"'))
        except SiteContent.DoesNotExist:
            self.stdout.write(self.style.WARNING('Invalid section "a1" not found'))
