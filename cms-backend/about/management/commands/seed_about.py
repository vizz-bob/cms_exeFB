from django.core.management.base import BaseCommand
from about.models import AboutPage, TeamMember, Award, TechStack

class Command(BaseCommand):
    help = 'Seeds the About Page content according to Document 2 structure'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding About Page Data...')

        # --- 1. COMPANY OVERVIEW & CORE CONTENT ---
        # Updated titles to match Document 2 (Company Overview, Mission, Vision, Values)
        about_data = {
            "hero_title": "About XpertAI Global",
            "hero_subtitle": "Redefining financial outsourcing with AI-powered precision and blockchain transparency.",
            
            # i. Company Overview
            "story_title": "Company Overview",
            "story_text": "XpertAI Global is a next-generation marketplace for financial outsourcing, connecting businesses with verified professionals through an AI-powered matching engine.\n\nWe record performance metrics on a blockchain ledger to ensure absolute trust and transparency. Our platform automates the traditional friction of hiring, managing, and auditing financial services.",
            # Note: The 'story_image' field in the CMS will serve as the "Infographic" placeholder
            
            # ii. Mission, Vision & Values
            "mission_title": "Our Mission",
            "mission_text": "To democratize high-end financial analytics and compliance for businesses globally through automation.",
            
            "vision_title": "Our Vision",
            "vision_text": "A world where financial trust is automated, and every business decision is data-driven.",
            
            "values_title": "Our Values",
            "values_text": "Transparency, Innovation, and Accuracy. We believe in code-enforced trust.",
            
            # Extra Sections (kept for completeness)
            "global_title": "Global Reach",
            "global_stats": "Serving Clients in 20+ Countries",
            "awards_title": "Awards & Recognition",
            "csr_title": "Sustainability & CSR",
            "csr_text": "Committed to green computing and paperless financial workflows.",
            "cta_title": "Join the Revolution",
            "cta_text": "Experience the future of finance today."
        }

        AboutPage.objects.update_or_create(id=1, defaults=about_data)
        self.stdout.write("   ✅ About Page Content Updated")

        # --- 2. LEADERSHIP & ADVISORY TEAM ---
        # iii. Leadership & Advisory Team
        team_data = [
            {"name": "Aditi Rao", "role": "Chief Executive Officer", "order": 1, "bio": "Ex-Goldman Sachs with 15 years in Fintech."},
            {"name": "Rajesh Kumar", "role": "Chief Technology Officer", "order": 2, "bio": "AI Researcher specializing in Large Language Models."},
            {"name": "Dr. Sarah Jenkins", "role": "Advisory Board Member", "order": 3, "bio": "Ph.D. in Forensic Accounting & Blockchain Ethics."},
            {"name": "Michael Chen", "role": "Head of Finance", "order": 4, "bio": "CPA with a decade of experience in cross-border tax."},
        ]

        # Clear existing to ensure clean slate
        TeamMember.objects.all().delete()
        
        for member in team_data:
            TeamMember.objects.create(
                name=member['name'],
                role=member['role'],
                order=member['order'],
                bio=member.get('bio', '')
            )
        self.stdout.write("   ✅ Leadership & Advisory Team Updated")

        # --- 3. TECHNOLOGY STACK ---
        # iv. Technology Stack (AI, Automation, Blockchain)
        tech_data = [
            {
                "title": "Artificial Intelligence",
                "description": "Proprietary ML matching engine and predictive analytics.",
                "icon_name": "BrainCircuit",
                "order": 1
            },
            {
                "title": "Robotic Automation",
                "description": "RPA bots for reconciliation and compliance filings.",
                "icon_name": "Bot",
                "order": 2
            },
            {
                "title": "Blockchain Ledger",
                "description": "Immutable performance and transaction recording.",
                "icon_name": "Link",
                "order": 3
            },
            {
                "title": "Secure Cloud",
                "description": "Bank-grade encryption and global data availability.",
                "icon_name": "Cloud",
                "order": 4
            }
        ]

        TechStack.objects.all().delete()

        for item in tech_data:
            TechStack.objects.create(
                title=item['title'],
                description=item['description'],
                icon_name=item['icon_name'],
                order=item['order']
            )
        self.stdout.write("   ✅ Technology Stack Updated")

        # --- 4. AWARDS (Optional/Extra) ---
        awards_data = [
            {"title": "Best Fintech Innovation", "year": "2024", "description": "Global Finance Summit"},
            {"title": "AI Excellence Award", "year": "2023", "description": "TechCrunch Disrupt"},
        ]
        Award.objects.all().delete()
        for award in awards_data:
            Award.objects.create(**award)
        self.stdout.write("   ✅ Awards Updated")

        self.stdout.write(self.style.SUCCESS('\n🎉 About Page Seeded According to Doc 2!'))