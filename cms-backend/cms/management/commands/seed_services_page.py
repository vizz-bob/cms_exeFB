from django.core.management.base import BaseCommand
from services_page.models import ServiceHero, ServiceCTA

class Command(BaseCommand):
    help = 'Seeds data for the Services page'

    def handle(self, *args, **kwargs):
        # Hero
        if ServiceHero.objects.count() == 0:
            ServiceHero.objects.create(
                title="Our Services",
                subtitle="End-to-end financial solutions tailored for your growth."
            )
        
        # CTA
        if ServiceCTA.objects.count() == 0:
            ServiceCTA.objects.create(
                title="Looking for a Custom Financial Solution?",
                text="Our experts are ready to help you design, deploy, and optimize your finance strategy.",
                button_text="Get a Custom Quote"
            )

        self.stdout.write(self.style.SUCCESS('✅ Services Page Seeded!'))