from django.core.management.base import BaseCommand
from django.utils.text import slugify  # <-- Ye import zaroori hai
from cms.models import Service, CaseStudy, Resource, SiteContent
from careers.models import JobOpening

class Command(BaseCommand):
    help = 'Seeds database with initial data for Services, Careers, Resources, and Home Page'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # --- 1. HOME PAGE CONTENT (Fixed Logic) ---
        home_content = [
            {"section_name": "hero_title", "title": "Innovate. Automate. Elevate.", "content": ""},
            {"section_name": "hero_text", "title": "", "content": "Empowering global enterprises with AI-driven financial intelligence. Streamline audits, optimize tax strategies, and forecast with precision."},
            {"section_name": "cta_button", "title": "", "content": "Schedule a Consultation"},
            {"section_name": "features_title", "title": "The XpertAI Advantage", "content": ""},
            {"section_name": "feature1_title", "title": "Predictive Analytics", "content": ""},
            {"section_name": "feature1_desc", "title": "", "content": "Forecast market trends and cash flow with 99% accuracy using our proprietary AI models."},
            {"section_name": "feature2_title", "title": "Automated Compliance", "content": ""},
            {"section_name": "feature2_desc", "title": "", "content": "Stay ahead of regulatory changes with real-time monitoring and automated reporting systems."},
            {"section_name": "feature3_title", "title": "Bank-Grade Security", "content": ""},
            {"section_name": "feature3_desc", "title": "", "content": "Your sensitive financial data is protected by military-grade encryption and 24/7 threat monitoring."},
            {"section_name": "hero_image", "title": "", "content": ""}, # Placeholder for image
        ]

        for item in home_content:
            # Slug generate karke lookup karenge taaki duplicate na bane
            target_slug = slugify(item['section_name'])
            
            SiteContent.objects.update_or_create(
                page="home",
                section=target_slug,  # <--- Yahan Change Hai: Slug se match kar rahe hain
                defaults={
                    "section_name": item['section_name'],
                    "title": item['title'],
                    "content": item['content']
                }
            )
        self.stdout.write(self.style.SUCCESS('✅ Home Page Content added!'))

        # --- 2. SERVICES ---
        services_data = [
            {
                "title": "Virtual CFO",
                "slug": "virtual-cfo",
                "short_description": "Strategic financial leadership without the overhead. Get expert guidance on budgeting, forecasting, and growth strategies.",
                "full_description": "<h3>Strategic Financial Leadership</h3><p>Our Virtual CFO service provides high-level financial strategy, budgeting, and forecasting. We help you navigate complex financial landscapes, ensuring your business remains profitable and compliant.</p><ul><li>Financial Planning & Analysis</li><li>Cash Flow Management</li><li>Risk Assessment</li></ul>",
                "icon": "Briefcase"
            },
            {
                "title": "Audit & Assurance",
                "slug": "audit-assurance",
                "short_description": "Comprehensive audits to ensure compliance, transparency, and build unshakeable trust with your stakeholders.",
                "full_description": "<h3>Unquestionable Integrity</h3><p>We provide rigorous audit services to ensure your financial statements are accurate and comply with all regulatory standards. Our approach is designed to add value and improve your business operations.</p><ul><li>Internal Audits</li><li>Statutory Audits</li><li>Fraud Investigation</li></ul>",
                "icon": "ShieldCheck"
            },
            {
                "title": "Taxation Services",
                "slug": "taxation-services",
                "short_description": "Optimize GST, TDS, and corporate tax management with our simplified, AI-driven compliance workflows.",
                "full_description": "<h3>Smart Tax Management</h3><p>Navigate the complexities of direct and indirect taxes with ease. Our experts ensure you maximize your savings while remaining 100% compliant with the latest tax laws.</p><ul><li>GST Filing & Compliance</li><li>Corporate Tax Planning</li><li>International Taxation</li></ul>",
                "icon": "FileText"
            }
        ]

        for item in services_data:
            Service.objects.get_or_create(slug=item['slug'], defaults=item)
        self.stdout.write(self.style.SUCCESS('✅ Services added!'))

        # --- 3. JOBS (CAREERS) ---
        jobs_data = [
            {
                "title": "Senior React Developer",
                "department": "Technology",
                "location": "Remote",
                "type": "Full-Time",
                "description": "We are looking for an experienced React developer to build scalable frontend applications. Must have experience with Tailwind CSS and API integration.",
                "is_active": True
            },
            {
                "title": "Financial Analyst",
                "department": "Finance",
                "location": "Mumbai",
                "type": "Full-Time",
                "description": "Analyze financial data and create financial models for decision support. CPA or MBA preferred.",
                "is_active": True
            }
        ]

        for item in jobs_data:
            JobOpening.objects.get_or_create(title=item['title'], defaults=item)
        self.stdout.write(self.style.SUCCESS('✅ Jobs added!'))

        # --- 4. CASE STUDIES ---
        case_studies = [
            {
                "title": "Tech Startup Scaling",
                "client_name": "InnoTech Solutions",
                "summary": "Helped a Series-B startup streamline their financial operations and prepare for the next funding round.",
                "result_stat": "300% Growth"
            },
            {
                "title": "Manufacturing Efficiency",
                "client_name": "SteelWorks Corp",
                "summary": "Implemented automated auditing systems to reduce manual errors and save costs significantly.",
                "result_stat": "40% Cost Saving"
            }
        ]

        for item in case_studies:
            CaseStudy.objects.get_or_create(title=item['title'], defaults=item)
        self.stdout.write(self.style.SUCCESS('✅ Case Studies added!'))

        # --- 5. RESOURCES ---
        resources = [
            {
                "title": "Financial Planning Guide 2025",
                "type": "E-Book",
                "description": "A comprehensive guide to planning your finances for the next fiscal year."
            },
            {
                "title": "Audit Checklist Template",
                "type": "Guide",
                "description": "Ensure you are ready for your next internal audit with this checklist."
            }
        ]

        for item in resources:
            Resource.objects.get_or_create(title=item['title'], defaults=item)
        self.stdout.write(self.style.SUCCESS('✅ Resources added!'))