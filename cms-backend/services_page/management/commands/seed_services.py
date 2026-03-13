from django.core.management.base import BaseCommand
from services_page.models import (
    ServiceHero, ServiceProcess, ServiceFeature, 
    ServiceTestimonial, ServiceFAQ, ServiceCTA
)

class Command(BaseCommand):
    help = 'Seeds the Services Page with rich dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Services Page Data...')

        # --- 1. HERO SECTION ---
        hero_data = {
            "title": "Comprehensive Financial Solutions",
            "subtitle": "From automated auditing to strategic CFO services, we provide the financial intelligence your business needs to scale.",
            "cta_text": "Explore Our Services"
        }
        ServiceHero.objects.update_or_create(id=1, defaults=hero_data)
        self.stdout.write("   ✅ Hero Section Updated")

        # --- 2. PROCESS STEPS ---
        processes = [
            {"step_number": "01", "title": "Discovery", "description": "We analyze your current financial infrastructure and identify gaps.", "icon_name": "Search", "order": 1},
            {"step_number": "02", "title": "Strategy", "description": "Our experts design a custom automation and compliance roadmap.", "icon_name": "Map", "order": 2},
            {"step_number": "03", "title": "Implementation", "description": "We deploy AI tools and integrate them with your existing ERPs.", "icon_name": "Settings", "order": 3},
            {"step_number": "04", "title": "Optimization", "description": "Continuous monitoring and reporting to ensure peak performance.", "icon_name": "TrendingUp", "order": 4},
        ]
        for p in processes:
            ServiceProcess.objects.update_or_create(title=p['title'], defaults=p)
        self.stdout.write("   ✅ Process Steps Added")

        # --- 3. FEATURES ---
        features = [
            {"title": "AI-Driven Accuracy", "description": "Reduce human error by 99% with our machine learning algorithms.", "icon_name": "CheckCircle", "order": 1},
            {"title": "Real-Time Reporting", "description": "Access live dashboards for cash flow, taxes, and p&l statements.", "icon_name": "BarChart2", "order": 2},
            {"title": "Bank-Grade Security", "description": "Your data is encrypted with AES-256 standards and SOC2 compliant.", "icon_name": "Shield", "order": 3},
            {"title": "Scalable Architecture", "description": "Our systems grow with you, handling millions of transactions effortlessly.", "icon_name": "Layers", "order": 4},
        ]
        for f in features:
            ServiceFeature.objects.update_or_create(title=f['title'], defaults=f)
        self.stdout.write("   ✅ Features Added")

        # --- 4. TESTIMONIALS ---
        testimonials = [
            {"name": "Michael Ross", "role": "CFO, TechFlow", "quote": "The virtual CFO service provided insights that saved us $200k in the first quarter alone.", "order": 1},
            {"name": "Anita Roy", "role": "Founder, UrbanStyle", "quote": "Automating our tax compliance was the best decision. XpertAI made it seamless.", "order": 2},
        ]
        for t in testimonials:
            ServiceTestimonial.objects.update_or_create(name=t['name'], defaults=t)
        self.stdout.write("   ✅ Testimonials Added")

        # --- 5. FAQS ---
        faqs = [
            {"question": "How long does implementation take?", "answer": "Typically 2-4 weeks depending on the complexity of your data.", "order": 1},
            {"question": "Can I integrate with QuickBooks/Xero?", "answer": "Yes, we have native integrations for all major accounting platforms.", "order": 2},
            {"question": "Is my data safe?", "answer": "Absolutely. We use military-grade encryption and regular security audits.", "order": 3},
            {"question": "Do you offer custom pricing?", "answer": "Yes, we have enterprise plans tailored to specific business needs.", "order": 4},
        ]
        for q in faqs:
            ServiceFAQ.objects.update_or_create(question=q['question'], defaults=q)
        self.stdout.write("   ✅ FAQs Added")

        # --- 6. CTA ---
        cta_data = {
            "title": "Ready to Optimize Your Finance Stack?",
            "text": "Book a free consultation with our experts and see the difference.",
            "button_text": "Get Started Now"
        }
        ServiceCTA.objects.update_or_create(id=1, defaults=cta_data)
        self.stdout.write("   ✅ Bottom CTA Updated")

        self.stdout.write(self.style.SUCCESS('\n🎉 Services Page Data Populated Successfully!'))