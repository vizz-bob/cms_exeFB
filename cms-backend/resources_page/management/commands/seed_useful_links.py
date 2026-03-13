from django.core.management.base import BaseCommand
from resources_page.models import UsefulLink

class Command(BaseCommand):
    help = 'Seeds Useful Links for the Resources Page'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Useful Links...')

        links_data = [
            {"title": "ICAI (Institute of Chartered Accountants of India)", "url": "https://www.icai.org/", "order": 1},
            {"title": "ICMAI (Institute of Cost Accountants of India)", "url": "https://icmai.in/", "order": 2},
            {"title": "ICSI (Institute of Company Secretaries of India)", "url": "https://www.icsi.edu/", "order": 3},
            {"title": "Income Tax Department", "url": "https://www.incometax.gov.in/", "order": 4},
            {"title": "Income Tax Rules (Taxmann)", "url": "https://www.taxmann.com/", "order": 5},
            {"title": "SEBI (Securities and Exchange Board of India)", "url": "https://www.sebi.gov.in/", "order": 6},
            {"title": "RBI (Reserve Bank of India)", "url": "https://rbi.org.in/", "order": 7},
            {"title": "MCA (Ministry of Corporate Affairs)", "url": "https://www.mca.gov.in/", "order": 8},
            {"title": "GST Portal", "url": "https://www.gst.gov.in/", "order": 9},
        ]

        for item in links_data:
            UsefulLink.objects.update_or_create(
                title=item['title'],
                defaults={'url': item['url'], 'order': item['order']}
            )
            self.stdout.write(f"   ✅ Added: {item['title']}")

        self.stdout.write(self.style.SUCCESS('🎉 Useful Links Seeded Successfully!'))