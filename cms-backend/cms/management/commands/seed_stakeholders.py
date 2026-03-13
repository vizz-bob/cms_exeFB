from django.core.management.base import BaseCommand
from stakeholders.models import Stakeholder

class Command(BaseCommand):
    help = 'Seeds data for the Stakeholders app'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Stakeholders Data...')

        stakeholders_data = [
            {
                "title": "Corporate Clients",
                "description": "Large enterprises leveraging our AI for audit automation and financial forecasting to drive efficiency.",
                "order": 1
            },
            {
                "title": "SME Partners",
                "description": "Small and medium businesses optimizing tax workflows, compliance, and cash flow management.",
                "order": 2
            },
            {
                "title": "Financial Institutions",
                "description": "Banks, insurance firms, and fintechs integrating our advanced security and fraud detection modules.",
                "order": 3
            },
            {
                "title": "Government Agencies",
                "description": "Public sector bodies utilizing our transparency tools for regulatory oversight and automated reporting.",
                "order": 4
            },
            {
                "title": "Investors & Shareholders",
                "description": "Key stakeholders driving our innovation roadmap, strategic growth, and global expansion.",
                "order": 5
            },
            {
                "title": "Technology Partners",
                "description": "Cloud infrastructure providers and AI research labs collaborating on next-gen financial tech.",
                "order": 6
            }
        ]

        for item in stakeholders_data:
            Stakeholder.objects.update_or_create(
                title=item['title'],
                defaults={
                    "description": item['description'],
                    "order": item['order']
                }
            )
            self.stdout.write(f"   ✅ Added: {item['title']}")

        self.stdout.write(self.style.SUCCESS('🎉 Stakeholders Data Successfully Seeded! Refresh your website.'))