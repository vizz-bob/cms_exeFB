from django.core.management.base import BaseCommand
from lead_system_page.models import LSHero, LSFeature, LSBottomCTA, LSDashboard

class Command(BaseCommand):
    help = 'Seeds data for Lead System Page'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Lead System Page...')

        # Hero
        if LSHero.objects.count() == 0:
            LSHero.objects.create(
                title="Intelligent Lead Management Engine",
                subtitle="Stop losing potential clients. Our AI-driven system captures, qualifies, and nurtures leads automatically."
            )

        # Features
        features = [
            {"title": "Automated Capture", "description": "Instantly capture leads from web forms and chatbots.", "icon_name": "Target", "order": 1},
            {"title": "Pipeline Tracking", "description": "Visualize your sales funnel with dynamic dashboards.", "icon_name": "BarChart3", "order": 2},
            {"title": "Smart Workflows", "description": "Never miss a follow-up with automated sequences.", "icon_name": "Zap", "order": 3},
        ]
        for f in features:
            LSFeature.objects.update_or_create(title=f['title'], defaults=f)

        # --- NEW: Dashboard Seed ---
        if LSDashboard.objects.count() == 0:
            LSDashboard.objects.create(
                placeholder_text="Analytics Dashboard (Upload Image in Admin)"
            )
        # ---------------------------

        # CTA
        if LSBottomCTA.objects.count() == 0:
            LSBottomCTA.objects.create(
                title="Ready to 10x Your Conversion?",
                text="Join over 500+ enterprises optimizing their sales pipeline.",
                button_text="Get Started Now"
            )

        self.stdout.write(self.style.SUCCESS('✅ Lead System Page Seeded!'))