from django.core.management.base import BaseCommand
from cms.models import SiteContent

class Command(BaseCommand):
    help = 'Seeds the database with initial data for the about page.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding about page data...')

        about_page_content = [
            {'section': 'about_hero_title', 'title': 'About Us'},
            {'section': 'about_hero_text', 'content': 'We are a team of passionate individuals dedicated to providing the best service to our clients.'},
            {'section': 'our_story_title', 'title': 'Our Story'},
            {'section': 'our_story_text', 'content': 'Our company was founded in 2024 with a mission to revolutionize the industry. We have been working hard ever since to achieve our goals.'},
        ]

        for item in about_page_content:
            SiteContent.objects.update_or_create(
                page='about',
                section=item['section'],
                defaults={
                    'title': item.get('title', ''),
                    'content': item.get('content', '')
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded about page data.'))