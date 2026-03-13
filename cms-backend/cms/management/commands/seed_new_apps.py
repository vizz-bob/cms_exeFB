from django.core.management.base import BaseCommand
from homepage.models import HeroSection, Stat, Feature, BottomCTA
from resources_page.models import ResourcesHero, SectionTitles, CaseStudy, DownloadableResource

class Command(BaseCommand):
    help = 'Seeds data for the new Homepage and Resources apps'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Dynamic Pages Data...')

        # ==========================================
        # 1. HOME PAGE POPULATION
        # ==========================================
        self.stdout.write('   🏠 Populating Home Page...')
        
        # --- Hero Section ---
        if HeroSection.objects.count() == 0:
            HeroSection.objects.create(
                title="Next-Gen Financial Intelligence for Global Enterprises",
                subtitle="Stop relying on outdated spreadsheets. XpertAI Global automates your auditing, tax compliance, and financial forecasting with 99.9% accuracy using proprietary AI models.",
                cta_text="Start Your Free Audit"
            )
            self.stdout.write("      ✅ Added Hero Section")
        
        # --- Stats ---
        stats_data = [
            {"value": "1,200+", "label": "Enterprise Clients", "order": 1},
            {"value": "$500M+", "label": "Assets Optimized", "order": 2},
            {"value": "99.9%", "label": "Compliance Accuracy", "order": 3},
        ]
        for item in stats_data:
            Stat.objects.update_or_create(label=item['label'], defaults=item)
        self.stdout.write("      ✅ Added Stats")

        # --- Features ---
        features_data = [
            {
                "title": "Predictive Financial Modeling",
                "description": "Don't just track expenses; forecast them. Our AI analyzes market trends to predict cash flow anomalies before they happen.",
                "icon_name": "TrendingUp",
                "order": 1
            },
            {
                "title": "Automated Regulatory Compliance",
                "description": "Navigate complex global tax laws effortlessly. Our system updates in real-time to keep your business 100% compliant.",
                "icon_name": "Shield",
                "order": 2
            },
            {
                "title": "Bank-Grade Security Shield",
                "description": "Your financial data is your most valuable asset. We protect it with military-grade encryption and 24/7 threat monitoring.",
                "icon_name": "Lock",
                "order": 3
            },
            {
                "title": "Real-Time Collaboration",
                "description": "Enable your entire finance team to work on the same data set simultaneously with role-based access controls.",
                "icon_name": "Users",
                "order": 4
            }
        ]
        for item in features_data:
            Feature.objects.update_or_create(title=item['title'], defaults=item)
        self.stdout.write("      ✅ Added Features")

        # --- Bottom CTA ---
        if BottomCTA.objects.count() == 0:
            BottomCTA.objects.create(
                title="Ready to Modernize Your Finance Stack?",
                text="Join the league of forward-thinking CFOs who are saving 40+ hours per week with XpertAI automation.",
                button_text="Schedule a Live Demo"
            )
            self.stdout.write("      ✅ Added Bottom CTA")

        # ==========================================
        # 2. RESOURCES PAGE POPULATION
        # ==========================================
        self.stdout.write('   📚 Populating Resources Page...')

        # --- Hero ---
        if ResourcesHero.objects.count() == 0:
            ResourcesHero.objects.create(
                title="Knowledge Center",
                subtitle="Explore our library of whitepapers, case studies, and guides to empower your financial journey."
            )
            self.stdout.write("      ✅ Added Resources Hero")

        # --- Section Titles ---
        if SectionTitles.objects.count() == 0:
            SectionTitles.objects.create(
                case_studies_title="Client Success Stories",
                downloads_title="Essential Downloads"
            )
            self.stdout.write("      ✅ Added Section Titles")

        # --- Case Studies ---
        studies_data = [
            {
                "title": "Tech Startup Scaling",
                "client_name": "InnoTech Solutions",
                "summary": "Helped a Series-B startup streamline their financial operations and prepare for the next funding round in just 3 months.",
                "result_stat": "300% Growth",
                "order": 1
            },
            {
                "title": "Manufacturing Efficiency",
                "client_name": "SteelWorks Corp",
                "summary": "Implemented automated auditing systems to reduce manual errors and save costs significantly across 5 factories.",
                "result_stat": "40% Cost Saving",
                "order": 2
            },
            {
                "title": "Retail Chain Optimization",
                "client_name": "FreshMart Retail",
                "summary": "Optimized inventory cash flow using predictive analytics, reducing waste and improving margins.",
                "result_stat": "2x Profit Margin",
                "order": 3
            }
        ]
        for item in studies_data:
            CaseStudy.objects.update_or_create(title=item['title'], defaults=item)
        self.stdout.write("      ✅ Added Case Studies")

        # --- Downloads ---
        downloads_data = [
            {
                "title": "Financial Planning Guide 2025",
                "resource_type": "E-Book",
                "description": "A comprehensive guide to planning your finances for the next fiscal year with AI insights.",
                "order": 1
            },
            {
                "title": "Audit Checklist Template",
                "resource_type": "Guide",
                "description": "Ensure you are ready for your next internal audit with this 50-point checklist.",
                "order": 2
            },
            {
                "title": "AI in Finance - Whitepaper",
                "resource_type": "Whitepaper",
                "description": "Understanding the impact of Artificial Intelligence on modern accounting practices.",
                "order": 3
            },
            {
                "title": "Global Tax Compliance Report",
                "resource_type": "Report",
                "description": "An analysis of tax regulation changes across 20 countries in the last year.",
                "order": 4
            }
        ]
        for item in downloads_data:
            DownloadableResource.objects.update_or_create(title=item['title'], defaults=item)
        self.stdout.write("      ✅ Added Downloadable Resources")

        self.stdout.write(self.style.SUCCESS('🎉 Successfully seeded data for Homepage and Resources App!'))