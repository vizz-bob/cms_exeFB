from django.core.management.base import BaseCommand
from careers.models import CareersPage, Benefit, JobOpening

class Command(BaseCommand):
    help = 'Seeds the Careers Page with rich data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Careers Page...')

        # 1. Page Content
        CareersPage.objects.update_or_create(id=1, defaults={
            "hero_title": "Build the Future of Finance",
            "hero_subtitle": "Join a team of visionaries, engineers, and financial experts redefining the global economy.",
            "benefits_title": "Why You'll Love It Here",
            "culture_text": "We believe in autonomy, mastery, and purpose. Work from anywhere, own your projects, and make a dent in the universe."
        })

        # 2. Benefits
        benefits = [
            {"title": "Remote First", "description": "Work from anywhere in the world.", "icon_name": "Globe", "order": 1},
            {"title": "Competitive Pay", "description": "Top-tier salary and equity packages.", "icon_name": "DollarSign", "order": 2},
            {"title": "Health & Wellness", "description": "Comprehensive insurance and gym stipends.", "icon_name": "Heart", "order": 3},
            {"title": "Learning Budget", "description": "$2000/year for courses and conferences.", "icon_name": "BookOpen", "order": 4},
        ]
        for b in benefits:
            Benefit.objects.update_or_create(title=b['title'], defaults=b)

        # 3. Jobs
        jobs = [
            {"title": "Senior Backend Engineer", "department": "Engineering", "location": "Remote", "type": "Full-Time", "description": "Build scalable APIs."},
            {"title": "Product Designer", "department": "Design", "location": "London / Remote", "type": "Full-Time", "description": "Craft beautiful user experiences."},
            {"title": "Marketing Manager", "department": "Marketing", "location": "New York", "type": "Full-Time", "description": "Lead our global growth campaigns."},
        ]
        for j in jobs:
            JobOpening.objects.update_or_create(title=j['title'], defaults=j)

        self.stdout.write(self.style.SUCCESS('🎉 Careers Page Seeded!'))