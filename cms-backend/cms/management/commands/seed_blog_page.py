from django.core.management.base import BaseCommand
from cms.models import SiteContent

class Command(BaseCommand):
    help = 'Seeds editable content for the Blog Page'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Blog Page Content...')

        blog_content = [
            # Hero Section
            {
                "section": "hero_title",
                "title": "Latest Insights & News",
                "content": ""
            },
            {
                "section": "hero_text",
                "title": "",
                "content": "Stay ahead of the curve with expert analysis, financial trends, and technology updates from XpertAI Global."
            },
            
            # Sidebar Labels
            {
                "section": "category_title",
                "title": "Filter by Category",
                "content": ""
            },
            {
                "section": "search_placeholder",
                "title": "Search Articles",
                "content": ""
            },
            
            # Main Area Label
            {
                "section": "latest_posts_title",
                "title": "Recent Articles",
                "content": ""
            },
        ]

        for item in blog_content:
            SiteContent.objects.update_or_create(
                page="blog",
                section=item["section"],
                defaults={
                    "title": item.get("title", ""),
                    "content": item.get("content", ""),
                    "section_name": item["section"].replace("_", " ").title()
                }
            )
            self.stdout.write(f"   ✅ Updated: {item['section']}")

        self.stdout.write(self.style.SUCCESS('🎉 Blog Page Data Updated! Check Admin Panel > Page: Blog Content'))