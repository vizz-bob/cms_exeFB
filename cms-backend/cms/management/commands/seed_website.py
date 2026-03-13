from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files.base import ContentFile

# Import Models from all Apps
from homepage.models import HeroSection, Stat, Feature, BottomCTA
from resources_page.models import ResourcesHero, SectionTitles, CaseStudy as ResourceCaseStudy, DownloadableResource
from stakeholders.models import Stakeholder
from cms.models import SiteContent, Service  # CMS Service Model
from careers.models import JobOpening
from blog.models import BlogCategory, BlogPost

class Command(BaseCommand):
    help = 'Populates the ENTIRE website with professional financial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Starting Full Website Population...')

        # ==========================================
        # 1. HOME PAGE (homepage app)
        # ==========================================
        self.stdout.write('   🏠 Seeding Home Page...')
        
        # Hero
        if HeroSection.objects.count() == 0:
            HeroSection.objects.create(
                title="Future-Proof Your Finances with AI Precision",
                subtitle="Join world-class enterprises in automating audits, tax compliance, and strategic forecasting. Experience 99.9% accuracy with XpertAI.",
                cta_text="Start Free Assessment"
            )
        
        # Stats
        stats = [
            {"value": "500+", "label": "Global Clients", "order": 1},
            {"value": "$2B+", "label": "Assets Managed", "order": 2},
            {"value": "40%", "label": "Cost Reduction", "order": 3},
        ]
        for s in stats:
            Stat.objects.update_or_create(label=s['label'], defaults=s)

        # Features
        features = [
            {"title": "Predictive Forecasting", "description": "AI models that predict cash flow trends and market shifts with high accuracy.", "icon_name": "TrendingUp", "order": 1},
            {"title": "Automated Audits", "description": "Reduce manual error and audit time by 70% with intelligent automated workflows.", "icon_name": "Shield", "order": 2},
            {"title": "Real-Time Compliance", "description": "Stay compliant with ever-changing global tax laws through auto-updated rule engines.", "icon_name": "FileCheck", "order": 3},
        ]
        for f in features:
            Feature.objects.update_or_create(title=f['title'], defaults=f)

        # Bottom CTA
        if BottomCTA.objects.count() == 0:
            BottomCTA.objects.create(
                title="Ready to Transform Your Finance Operation?",
                text="Book a demo today and see how XpertAI can save your team 20+ hours every week.",
                button_text="Book a Demo"
            )

        # ==========================================
        # 2. RESOURCES PAGE (resources_page app)
        # ==========================================
        self.stdout.write('   📚 Seeding Resources Page...')
        
        if ResourcesHero.objects.count() == 0:
            ResourcesHero.objects.create(
                title="Knowledge Hub",
                subtitle="Expert insights, whitepapers, and success stories to guide your financial strategy."
            )
        
        if SectionTitles.objects.count() == 0:
            SectionTitles.objects.create(
                case_studies_title="Client Success Stories",
                downloads_title="Industry Reports & Guides"
            )

        # Case Studies
        r_studies = [
            {"title": "Scaling FinTech Startup", "client_name": "PayFlow Inc.", "summary": "Automated reconciliation for 10M+ transactions daily.", "result_stat": "99.99% Uptime", "order": 1},
            {"title": "Retail Chain Audit", "client_name": "MartOne", "summary": "Reduced inventory shrinkage using predictive fraud detection.", "result_stat": "15% Margin Boost", "order": 2},
        ]
        for rs in r_studies:
            ResourceCaseStudy.objects.update_or_create(title=rs['title'], defaults=rs)

        # Downloads
        downloads = [
            {"title": "State of AI in Finance 2025", "resource_type": "Report", "description": "Global trends analysis.", "order": 1},
            {"title": "CFO's Guide to Automation", "resource_type": "Guide", "description": "Step-by-step implementation plan.", "order": 2},
            {"title": "Tax Compliance Checklist", "resource_type": "Whitepaper", "description": "Ensure you never miss a deadline.", "order": 3},
        ]
        for d in downloads:
            DownloadableResource.objects.update_or_create(title=d['title'], defaults=d)

        # ==========================================
        # 3. STAKEHOLDERS PAGE (stakeholders app)
        # ==========================================
        self.stdout.write('   🤝 Seeding Stakeholders...')
        holders = [
            {"title": "Corporate Clients", "description": "Enterprises streamlining audits and tax filings.", "order": 1},
            {"title": "SME Partners", "description": "Small businesses accessing CFO-level insights.", "order": 2},
            {"title": "Investors", "description": "Driving innovation in financial technology.", "order": 3},
            {"title": "Government Bodies", "description": "Ensuring regulatory transparency and compliance.", "order": 4},
            {"title": "Tech Integrators", "description": "Connecting ERPs with our AI engine.", "order": 5},
            {"title": "Consultants", "description": "Advisory firms leveraging our data.", "order": 6},
        ]
        for h in holders:
            Stakeholder.objects.update_or_create(title=h['title'], defaults=h)

        # ==========================================
        # 4. SERVICES (cms app models)
        # ==========================================
        self.stdout.write('   🛠️ Seeding Services...')
        services = [
            {"title": "Virtual CFO", "slug": "virtual-cfo", "short_description": "Strategic leadership on demand.", "full_description": "<p>Full financial strategy...</p>", "icon": "Briefcase", "order": 1},
            {"title": "Audit Automation", "slug": "audit-automation", "short_description": "Error-free compliance audits.", "full_description": "<p>Automated auditing...</p>", "icon": "ShieldCheck", "order": 2},
            {"title": "Tax Advisory", "slug": "tax-advisory", "short_description": "Optimize your tax liabilities.", "full_description": "<p>Tax planning...</p>", "icon": "FileText", "order": 3},
            {"title": "Risk Management", "slug": "risk-management", "short_description": "Identify financial risks early.", "full_description": "<p>Risk assessment...</p>", "icon": "AlertTriangle", "order": 4},
            {"title": "Payroll Systems", "slug": "payroll-systems", "short_description": "Seamless global payroll.", "full_description": "<p>Payroll management...</p>", "icon": "Users", "order": 5},
            {"title": "Wealth Management", "slug": "wealth-mgmt", "short_description": "Grow your corporate assets.", "full_description": "<p>Investment strategy...</p>", "icon": "TrendingUp", "order": 6},
        ]
        for srv in services:
            Service.objects.update_or_create(slug=srv['slug'], defaults=srv)

        # ==========================================
        # 5. CAREERS (careers app)
        # ==========================================
        self.stdout.write('   💼 Seeding Careers...')
        jobs = [
            {"title": "Senior AI Engineer", "department": "Engineering", "location": "Remote", "type": "Full-Time", "description": "Build next-gen financial models."},
            {"title": "Financial Analyst", "department": "Finance", "location": "New York", "type": "Full-Time", "description": "Analyze market trends."},
            {"title": "Marketing Lead", "department": "Marketing", "location": "London", "type": "Full-Time", "description": "Lead our global brand."},
        ]
        for job in jobs:
            JobOpening.objects.update_or_create(title=job['title'], defaults=job)

        # ==========================================
        # 6. BLOG (blog app)
        # ==========================================
        self.stdout.write('   📝 Seeding Blog...')
        # Categories
        cats = ["Finance Trends", "AI Technology", "Company News"]
        for c in cats:
            BlogCategory.objects.get_or_create(name=c)
        
        # Posts
        tech_cat = BlogCategory.objects.get(name="AI Technology")
        fin_cat = BlogCategory.objects.get(name="Finance Trends")
        
        posts = [
            {"title": "The Future of AI in Auditing", "category": tech_cat, "short_description": "How machine learning is replacing manual checks.", "body": "<p>Content here...</p>", "published": True},
            {"title": "5 Tax Saving Strategies for 2025", "category": fin_cat, "short_description": "Prepare your business for the new fiscal year.", "body": "<p>Content here...</p>", "published": True},
        ]
        for p in posts:
            BlogPost.objects.update_or_create(title=p['title'], defaults={**p, "slug": slugify(p['title'])})

        # ==========================================
        # 7. SITE CONTENT (cms app - Generic Pages)
        # ==========================================
        self.stdout.write('   📄 Seeding Page Headers (About, Contact, etc)...')
        
        generic_content = [
            # About Page
            {"page": "about", "section": "hero_title", "title": "About XpertAI Global"},
            {"page": "about", "section": "hero_text", "content": "We are pioneering the intersection of finance and artificial intelligence."},
            {"page": "about", "section": "mission_title", "title": "Our Mission"},
            {"page": "about", "section": "mission_text", "content": "To democratize access to high-end financial intelligence for businesses of all sizes."},
            
            # Contact Page
            {"page": "contact", "section": "contact_header", "title": "Get in Touch"},
            {"page": "contact", "section": "contact_subtext", "content": "Have a question? Our team is ready to help you optimize your finances."},
            {"page": "contact", "section": "address", "content": "123 Innovation Drive, Tech Park, NY"},
            {"page": "contact", "section": "email", "content": "hello@xpertai.global"},
            {"page": "contact", "section": "phone", "content": "+1 (555) 123-4567"},

            # Services Page Header
            {"page": "services", "section": "hero_title", "title": "Our Services"},
            {"page": "services", "section": "hero_text", "content": "Comprehensive financial solutions powered by advanced analytics."},
            
            # Careers Page Header
            {"page": "careers", "section": "hero_title", "title": "Join the Revolution"},
            {"page": "careers", "section": "hero_text", "content": "Build the future of finance with a team of visionaries."},
        ]

        for item in generic_content:
            SiteContent.objects.update_or_create(
                page=item['page'],
                section=item['section'],
                defaults={
                    "title": item.get('title', ''),
                    "content": item.get('content', ''),
                    "section_name": item['section'].replace("_", " ").title()
                }
            )

        self.stdout.write(self.style.SUCCESS('\n🎉 WEBSITE FULLY SEEDED! All pages are now populated with professional data.'))