from django.core.management.base import BaseCommand
from homepage.models import (
    HomePageContent, TrustedClient, Stat, 
    ProcessStep, Feature, Testimonial, FAQ
)

class Command(BaseCommand):
    help = 'Seeds the Home Page with 8+ Sections of rich data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Home Page...')

        # 1. Main Content (Singleton)
        content_data = {
            "hero_title": "The Operating System for Modern Finance",
            "hero_subtitle": "Unify your accounting, audit, and tax workflows with our AI-native platform. Designed for CFOs who demand precision.",
            "hero_cta_text": "Start Transformation",
            "clients_title": "Trusted by 500+ Enterprises",
            "process_title": "From Chaos to Clarity",
            "process_subtitle": "Our 3-step autonomous financial framework.",
            "features_title": "Why Global Leaders Choose XpertAI",
            "reviews_title": "What CFOs Are Saying",
            "faq_title": "Common Queries",
            "cta_title": "Ready to Automate Your Financial Future?",
            "cta_text": "Get a custom audit of your current financial stack today.",
            "cta_btn_text": "Book Consultation"
        }
        HomePageContent.objects.update_or_create(id=1, defaults=content_data)
        self.stdout.write("   ✅ Main Content Updated")

        # 2. Stats
        stats = [
            {"value": "10M+", "label": "Transactions Processed", "order": 1},
            {"value": "99.9%", "label": "Accuracy Rate", "order": 2},
            {"value": "45%", "label": "Cost Reduction", "order": 3},
            {"value": "24/7", "label": "Real-time Monitoring", "order": 4},
        ]
        for s in stats:
            Stat.objects.update_or_create(label=s['label'], defaults=s)
        self.stdout.write("   ✅ Stats Updated")

        # 3. Process Steps
        steps = [
            {"step_number": "01", "title": "Data Integration", "description": "Connect your ERPs and bank accounts securely in minutes.", "icon_name": "Link", "order": 1},
            {"step_number": "02", "title": "AI Analysis", "description": "Our models detect anomalies and opportunities instantly.", "icon_name": "Cpu", "order": 2},
            {"step_number": "03", "title": "Strategic Execution", "description": "Auto-generate reports and execute tax filings with one click.", "icon_name": "Rocket", "order": 3},
        ]
        for step in steps:
            ProcessStep.objects.update_or_create(title=step['title'], defaults=step)
        self.stdout.write("   ✅ Process Steps Updated")

        # 4. Features
        feats = [
            {"title": "Predictive Cash Flow", "description": "Forecast 12 months ahead with 95% confidence intervals.", "icon_name": "TrendingUp", "order": 1},
            {"title": "Automated Reconciliation", "description": "Match thousands of transactions in seconds, not days.", "icon_name": "RefreshCw", "order": 2},
            {"title": "Global Tax Compliance", "description": "Real-time updates for GST, VAT, and corporate tax laws.", "icon_name": "Globe", "order": 3},
            {"title": "Audit Trail Immutable", "description": "Blockchain-backed logs for every financial action taken.", "icon_name": "ShieldCheck", "order": 4},
        ]
        for f in feats:
            Feature.objects.update_or_create(title=f['title'], defaults=f)
        self.stdout.write("   ✅ Features Updated")

        # 5. Testimonials
        tests = [
            {"author_name": "Elena Rodriguez", "role": "CFO", "company": "TechNova Inc", "quote": "XpertAI reduced our month-end close time from 10 days to just 2. It's magic.", "order": 1},
            {"author_name": "David Kim", "role": "Founder", "company": "ScaleUp Partners", "quote": "The predictive insights saved us from a major cash flow crunch last quarter.", "order": 2},
        ]
        for t in tests:
            Testimonial.objects.update_or_create(author_name=t['author_name'], defaults=t)
        self.stdout.write("   ✅ Testimonials Updated")

        # 6. FAQs
        faqs = [
            {"question": "Is my financial data secure?", "answer": "Yes, we use bank-grade AES-256 encryption and are SOC2 Type II compliant.", "order": 1},
            {"question": "Can it integrate with SAP/Oracle?", "answer": "Absolutely. We have native connectors for all major ERPs including SAP, Oracle, and Xero.", "order": 2},
            {"question": "What is the implementation time?", "answer": "Most clients are fully live within 2-4 weeks depending on data volume.", "order": 3},
        ]
        for q in faqs:
            FAQ.objects.update_or_create(question=q['question'], defaults=q)
        self.stdout.write("   ✅ FAQs Updated")

        # 7. Trusted Clients (Placeholders)
        # Note: Images won't be created, just records. Upload images in Admin.
        clients = ["Google", "Amazon", "Stripe", "Shopify"]
        for i, c in enumerate(clients):
            TrustedClient.objects.get_or_create(name=c, defaults={"order": i})
        self.stdout.write("   ✅ Client Placeholders Added")

        self.stdout.write(self.style.SUCCESS('\n🎉 Home Page Revamp Seeded Successfully!'))