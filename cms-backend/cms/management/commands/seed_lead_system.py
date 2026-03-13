from django.core.management.base import BaseCommand
from cms.models import SiteContent

class Command(BaseCommand):
    help = 'Seeds professional data for the Lead System page'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Lead System Page...')

        data = [
            # Hero Section
            {
                "section": "hero_title",
                "title": "Intelligent Lead Management Engine",
                "content": ""
            },
            {
                "section": "hero_text",
                "title": "",
                "content": "Stop losing potential clients. Our AI-driven system captures, qualifies, and nurtures leads automatically."
            },

            # --- NEW: DASHBOARD DATA (Fixed) ---
            {
                # Ye entry missing thi, isliye image upload nahi dikh raha tha
                "section": "dashboard_image",
                "title": "Dashboard Preview Image",
                "content": "" 
            },
            {
                "section": "dashboard_text",
                "title": "",
                "content": "Interactive Analytics Dashboard (Upload Image in Admin)"
            },
            # ---------------------------

            # Feature Cards
            {
                "section": "ls_feature_1_title",
                "title": "Automated Capture & Scoring",
                "content": ""
            },
            {
                "section": "ls_feature_1_desc",
                "title": "",
                "content": "Instantly capture leads from web forms, chatbots, and emails. Our AI scores them based on engagement probability."
            },
            {
                "section": "ls_feature_2_title",
                "title": "Real-Time Pipeline Tracking",
                "content": ""
            },
            {
                "section": "ls_feature_2_desc",
                "title": "",
                "content": "Visualize your sales funnel with dynamic dashboards. Track every interaction from initial contact to final conversion."
            },
            {
                "section": "ls_feature_3_title",
                "title": "Smart Follow-up Workflows",
                "content": ""
            },
            {
                "section": "ls_feature_3_desc",
                "title": "",
                "content": "Never miss a follow-up. Set up automated email sequences and reminders tailored to lead behavior."
            },

            # CTA Section
            {
                "section": "cta_title",
                "title": "Ready to 10x Your Conversion Rate?",
                "content": ""
            },
            {
                "section": "cta_text",
                "title": "",
                "content": "Join over 500+ enterprises optimizing their sales pipeline with XpertAI."
            },
            {
                "section": "cta_button",
                "title": "Get Started Now",
                "content": ""
            },
        ]

        for item in data:
            SiteContent.objects.update_or_create(
                page="lead_system",
                section=item["section"],
                defaults={
                    "title": item.get("title", ""),
                    "content": item.get("content", ""),
                    "section_name": item["section"].replace("_", " ").title()
                }
            )
            self.stdout.write(f"   ✅ Updated: {item['section']}")

        self.stdout.write(self.style.SUCCESS('🎉 Lead System Page Populated Successfully!'))