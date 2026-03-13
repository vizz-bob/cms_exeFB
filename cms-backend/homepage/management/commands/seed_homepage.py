from django.core.management.base import BaseCommand
from homepage.models import (
    HomePageContent, TrustedClient, Stat, 
    ProcessStep, Feature, Testimonial, FAQ
)

class Command(BaseCommand):
    help = 'Seeds the Home Page with rich data including the new Automation Flow'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Home Page Data...')

        # --- 1. MAIN HERO CONTENT ---
        # This manages the main text on the home page
        content_data = {
            "hero_title": "Future of Financial Outsourcing",
            "hero_subtitle": "Experience the power of AI-driven precision, automated workflows, and blockchain-secured transparency for all your financial needs.",
            "hero_cta_text": "Get Started",
            "process_title": "Automation Flow",
            "process_subtitle": "Seamlessly connecting your needs to verified experts, secured by blockchain transparency.",
            "features_title": "Why Choose XpertAI?",
            "reviews_title": "Trusted by Leaders",
            "faq_title": "Frequently Asked Questions",
            "cta_title": "Ready to Optimize Your Finance?",
            "cta_text": "Join the next generation of financial intelligence today.",
            "cta_btn_text": "Contact Sales"
        }

        HomePageContent.objects.update_or_create(id=1, defaults=content_data)
        self.stdout.write("   ✅ Main Content Updated")

        # --- 2. STATS STRIP ---
        stats = [
            {"value": "500+", "label": "Global Clients", "order": 1},
            {"value": "98%", "label": "Accuracy Rate", "order": 2},
            {"value": "24/7", "label": "AI Availability", "order": 3},
            {"value": "$50M+", "label": "Funds Managed", "order": 4},
        ]
        
        for stat in stats:
            Stat.objects.update_or_create(
                label=stat['label'],
                defaults={"value": stat['value'], "order": stat['order']}
            )
        self.stdout.write("   ✅ Stats Updated")

        # --- 3. AUTOMATION FLOW (INFOGRAPHIC) ---
        # This dynamic section replaces the hardcoded frontend steps
        process_steps = [
            {
                "step_number": "01", 
                "title": "Client", 
                "description": "Submits Requirement", 
                "icon_name": "User", 
                "order": 1
            },
            {
                "step_number": "02", 
                "title": "AI Matching", 
                "description": "Finds Best Fit Pro", 
                "icon_name": "Cpu", 
                "order": 2
            },
            {
                "step_number": "03", 
                "title": "Verified Pro", 
                "description": "Executes Task", 
                "icon_name": "CheckCircle", 
                "order": 3
            },
            {
                "step_number": "04", 
                "title": "Blockchain", 
                "description": "Records Ledger", 
                "icon_name": "Link", # This maps to the Link/Chain icon
                "order": 4
            },
        ]

        # We clear existing steps first to ensure the order is perfect
        ProcessStep.objects.all().delete()
        
        for step in process_steps:
            ProcessStep.objects.create(**step)
        self.stdout.write("   ✅ Automation Flow Steps Updated")

        # --- 4. FEATURES ---
        features = [
            {"title": "Predictive Cash Flow", "description": "Forecast 12 months ahead with 95% confidence intervals.", "icon_name": "TrendingUp", "order": 1},
            {"title": "Automated Reconciliation", "description": "Match thousands of transactions in seconds, not days.", "icon_name": "RefreshCw", "order": 2},
            {"title": "Global Tax Compliance", "description": "Real-time updates for GST, VAT, and corporate tax laws.", "icon_name": "Globe", "order": 3},
            {"title": "Immutable Audit Trail", "description": "Blockchain-backed logs for every financial action taken.", "icon_name": "ShieldCheck", "order": 4},
        ]

        for feat in features:
            Feature.objects.update_or_create(
                title=feat['title'],
                defaults={
                    "description": feat['description'],
                    "icon_name": feat['icon_name'],
                    "order": feat['order']
                }
            )
        self.stdout.write("   ✅ Features Updated")

        # --- 5. TESTIMONIALS ---
        testimonials = [
            {
                "author_name": "Elena Rodriguez", 
                "role": "CFO", 
                "company": "TechNova Inc", 
                "quote": "XpertAI reduced our month-end close time from 10 days to just 2. It's magic.", 
                "order": 1
            },
            {
                "author_name": "David Kim", 
                "role": "Founder", 
                "company": "ScaleUp Partners", 
                "quote": "The predictive insights saved us from a major cash flow crunch last quarter.", 
                "order": 2
            },
        ]

        for t in testimonials:
            Testimonial.objects.update_or_create(
                author_name=t['author_name'],
                defaults=t
            )
        self.stdout.write("   ✅ Testimonials Updated")

        # --- 6. FAQs ---
        faqs = [
            {"question": "Is my financial data secure?", "answer": "Yes, we use bank-grade AES-256 encryption and are SOC2 Type II compliant.", "order": 1},
            {"question": "Can it integrate with SAP/Oracle?", "answer": "Absolutely. We have native connectors for all major ERPs including SAP, Oracle, and Xero.", "order": 2},
            {"question": "What is the implementation time?", "answer": "Most clients are fully live within 2-4 weeks depending on data volume.", "order": 3},
            {"question": "How does the blockchain ledger work?", "answer": "Every completed task and transaction is hashed and recorded on a private blockchain, ensuring an unalterable audit trail.", "order": 4},
        ]

        for q in faqs:
            FAQ.objects.update_or_create(
                question=q['question'],
                defaults=q
            )
        self.stdout.write("   ✅ FAQs Updated")

        # --- 7. TRUSTED CLIENTS ---
        # Simple placeholder clients
        clients = ["Google", "Amazon", "Stripe", "Shopify", "Microsoft"]
        for i, client_name in enumerate(clients):
            TrustedClient.objects.get_or_create(
                name=client_name,
                defaults={"order": i}
            )
        self.stdout.write("   ✅ Trusted Clients Updated")

        self.stdout.write(self.style.SUCCESS('\n🎉 Home Page & Automation Flow Seeded Successfully!'))