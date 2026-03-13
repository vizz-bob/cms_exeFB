from django.core.management.base import BaseCommand
from legal.models import LegalPage

class Command(BaseCommand):
    help = 'Seeds initial Terms and Privacy pages'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Legal Pages...')

        pages = [
            {
                "title": "Privacy Policy",
                "slug": "privacy-policy",
                "content": """
                    <h2>1. Introduction</h2>
                    <p>Welcome to XpertAI Global. We respect your privacy and are committed to protecting your personal data.</p>
                    <h2>2. Data We Collect</h2>
                    <p>We may collect personal data such as your name, email address, and phone number when you use our services.</p>
                    <h2>3. How We Use Your Data</h2>
                    <p>We use your data to provide and improve our services, communicate with you, and comply with legal obligations.</p>
                    <h2>4. Contact Us</h2>
                    <p>If you have any questions, please contact us at support@xpertai.global.</p>
                """
            },
            {
                "title": "Terms of Service",
                "slug": "terms-and-conditions",
                "content": """
                    <h2>1. Acceptance of Terms</h2>
                    <p>By accessing and using our website, you accept and agree to be bound by the terms and provision of this agreement.</p>
                    <h2>2. Use License</h2>
                    <p>Permission is granted to temporarily download one copy of the materials on XpertAI Global's website for personal, non-commercial transitory viewing only.</p>
                    <h2>3. Disclaimer</h2>
                    <p>The materials on XpertAI Global's website are provided on an 'as is' basis.</p>
                """
            }
        ]

        for p in pages:
            LegalPage.objects.update_or_create(
                slug=p['slug'],
                defaults={'title': p['title'], 'content': p['content']}
            )
            self.stdout.write(f"   ✅ Created/Updated: {p['title']}")

        self.stdout.write(self.style.SUCCESS('🎉 Legal Pages Seeded Successfully!'))
