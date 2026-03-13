from django.core.management.base import BaseCommand
from legal.models import LegalPage, LegalPageSection

class Command(BaseCommand):
    help = 'Seeds initial Legal Pages (Privacy, Terms, Refund)'

    def handle(self, *args, **kwargs):
        pages = [
            {
                "title": "Privacy Policy", 
                "slug": "privacy-policy",
                "description": "Your privacy is important to us. This policy explains how we handle your data."
            },
            {
                "title": "Terms and Conditions", 
                "slug": "terms-and-conditions",
                "description": "Please read these terms carefully before using our services."
            },
            {
                "title": "Refund Policy", 
                "slug": "refund-policy",
                "description": "Our policy regarding refunds, cancellations, and returns."
            },
        ]

        self.stdout.write("🚀 Seeding Legal Pages...")

        for p in pages:
            page, created = LegalPage.objects.get_or_create(
                slug=p['slug'],
                defaults={
                    'title': p['title'],
                    'description': p['description']
                }
            )
            
            if created:
                self.stdout.write(f"   ✅ Created Page: {p['title']}")
                # Add a default section so it's not empty
                LegalPageSection.objects.create(
                    legal_page=page,
                    heading="1. Introduction",
                    content="Welcome. This is a placeholder section. You can edit this from the Admin Panel.",
                    order=1
                )
            else:
                self.stdout.write(f"   ℹ️  Exists: {p['title']}")

        self.stdout.write(self.style.SUCCESS("🎉 Legal Data Seeded Successfully!"))