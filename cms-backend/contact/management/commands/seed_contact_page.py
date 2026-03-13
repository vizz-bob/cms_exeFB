from django.core.management.base import BaseCommand
from contact.models import ContactPage, OfficeAddress

class Command(BaseCommand):
    help = 'Seeds Contact Page Data with Noida Location'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Contact Page...')

        # 1. Page Content (Noida Map)
        ContactPage.objects.update_or_create(id=1, defaults={
            "hero_title": "Contact Us",
            "hero_subtitle": "We are here to help you with your financial outsourcing needs.",
            "form_title": "Start Your Transformation",
            "support_title": "Support Centre",
            "support_text": "Need quick help? Raise a ticket or chat with us.",
            # Noida Map Embed URL
            "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d224345.83923192776!2d77.2089851!3d28.5272803!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390ce5a43173357b%3A0x10524328e91fefd1!2sNoida%2C%20Uttar%20Pradesh!5e0!3m2!1sen!2sin!4v1700000000000!5m2!1sen!2sin"
        })

        # 2. Office Addresses (Noida Only)
        addresses = [
            {
                "title": "Corporate Headquarters",
                "address": "Floor 5, Tech Boulevard, Sector 127, Noida, Uttar Pradesh - 201301",
                "phone": "+91 120 456 7890",
                "email": "corporate@xpertai.global",
                "order": 1
            },
            {
                "title": "Development Center",
                "address": "Express Trade Tower, Sector 132, Noida, Uttar Pradesh - 201304",
                "phone": "+91 120 987 6543",
                "email": "tech@xpertai.global",
                "order": 2
            }
        ]
        
        OfficeAddress.objects.all().delete()
        for addr in addresses:
            OfficeAddress.objects.create(**addr)

        self.stdout.write(self.style.SUCCESS('🎉 Contact Page Seeded with Noida Details!'))