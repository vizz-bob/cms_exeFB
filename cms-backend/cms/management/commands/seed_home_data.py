from django.core.management.base import BaseCommand
from cms.models import SiteContent

class Command(BaseCommand):
    help = 'Populates the Home Page with rich, professional data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Populating Home Page with Rich Data...')

        home_data = [
            # --- 1. HERO SECTION ---
            {
                "section": "hero_title",
                "title": "Next-Gen Financial Intelligence for Global Enterprises",
                "content": ""
            },
            {
                "section": "hero_text",
                "title": "",
                "content": "Stop relying on outdated spreadsheets. XpertAI Global automates your auditing, tax compliance, and financial forecasting with 99.9% accuracy using proprietary AI models."
            },
            {
                "section": "cta_button",
                "title": "",
                "content": "Start Your Free Audit"
            },

            # --- 2. STATS STRIP ---
            {"section": "stat1_value", "title": "500+", "content": ""},
            {"section": "stat1_label", "title": "Enterprise Clients", "content": ""},
            
            {"section": "stat2_value", "title": "$10M+", "content": ""},
            {"section": "stat2_label", "title": "Revenue Optimized", "content": ""},
            
            {"section": "stat3_value", "title": "100%", "content": ""},
            {"section": "stat3_label", "title": "Audit Compliance", "content": ""},

            # --- 3. SERVICES PREVIEW ---
            {
                "section": "services_title",
                "title": "Our Core Expertise",
                "content": ""
            },
            {
                "section": "service1_title",
                "title": "Virtual CFO",
                "content": ""
            },
            {
                "section": "service1_desc",
                "title": "",
                "content": "Strategic financial planning and cash flow management without the overhead of a full-time executive."
            },
            {
                "section": "service2_title",
                "title": "Audit & Assurance",
                "content": ""
            },
            {
                "section": "service2_desc",
                "title": "",
                "content": "AI-driven internal and statutory audits that ensure zero-error compliance and total transparency."
            },
            {
                "section": "service3_title",
                "title": "Taxation Advisory",
                "content": ""
            },
            {
                "section": "service3_desc",
                "title": "",
                "content": "Optimize your GST, TDS, and corporate tax liabilities with our automated tax planning engines."
            },

            # --- 4. FEATURES SECTION ---
            {
                "section": "features_title",
                "title": "Why Industry Leaders Trust XpertAI",
                "content": ""
            },
            {
                "section": "feature1_title",
                "title": "Predictive Analytics",
                "content": ""
            },
            {
                "section": "feature1_desc",
                "title": "",
                "content": "Don't just track expenses; forecast them. Our AI analyzes market trends to predict cash flow anomalies before they happen."
            },
            {
                "section": "feature2_title",
                "title": "Automated Compliance",
                "content": ""
            },
            {
                "section": "feature2_desc",
                "title": "",
                "content": "Navigate complex global tax laws effortlessly. Our system updates in real-time to keep your business 100% compliant."
            },
            {
                "section": "feature3_title",
                "title": "Bank-Grade Security",
                "content": ""
            },
            {
                "section": "feature3_desc",
                "title": "",
                "content": "Your financial data is your most valuable asset. We protect it with military-grade encryption and 24/7 threat monitoring."
            },

            # --- 5. TESTIMONIALS ---
            {
                "section": "testimonials_title",
                "title": "What Our Clients Say",
                "content": ""
            },
            {
                "section": "testimonial1_text",
                "title": "",
                "content": "XpertAI transformed our audit process. What used to take weeks now happens in days with higher accuracy."
            },
            {
                "section": "testimonial1_author",
                "title": "Rajesh Kumar, CEO of TechFin",
                "content": ""
            },
            {
                "section": "testimonial2_text",
                "title": "",
                "content": "The Virtual CFO service gave us the financial clarity we needed to secure our Series B funding."
            },
            {
                "section": "testimonial2_author",
                "title": "Sarah Jenkins, Founder of StartUp Hub",
                "content": ""
            },
            {
                "section": "testimonial3_text",
                "title": "",
                "content": "Their automated tax filing saved us over 15% in penalties and optimized our returns significantly."
            },
            {
                "section": "testimonial3_author",
                "title": "Amit Patel, Director at OmniCorp",
                "content": ""
            },

            # --- 6. BOTTOM CTA SECTION ---
            {
                "section": "cta_title",
                "title": "Ready to Modernize Your Finance Stack?",
                "content": ""
            },
            {
                "section": "cta_text",
                "title": "",
                "content": "Join the league of forward-thinking businesses saving 40+ hours per week with XpertAI automation."
            },
            {
                "section": "cta_button_text",
                "title": "Schedule a Live Demo",
                "content": ""
            },
        ]

        for item in home_data:
            # Generate a readable name for the admin panel
            readable_name = item["section"].replace("_", " ").title()
            
            SiteContent.objects.update_or_create(
                page="home",
                section=item["section"],
                defaults={
                    "title": item.get("title", ""),
                    "content": item.get("content", ""),
                    "section_name": readable_name
                }
            )
            self.stdout.write(f"   ✅ Updated: {item['section']}")

        self.stdout.write(self.style.SUCCESS('🎉 Home Page Data Successfully Updated! Refresh your website.'))