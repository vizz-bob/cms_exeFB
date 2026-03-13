from django.core.management.base import BaseCommand
from django.utils import timezone
from cms.models import SiteContent, Service, CaseStudy, Resource
from blog.models import BlogPost
from careers.models import JobOpening, JobApplication
from leads.models import Lead, NewsletterSubscriber
from contact.models import ContactMessage
from theme.models import ThemeSetting
from cms.sections import PAGE_SECTIONS
import random

class Command(BaseCommand):
    help = 'Seeds the database with dummy data for ALL empty sections.'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Starting Full Database Seeding...')

        # --- 1. SEED CMS CONTENT (ALL PAGES) ---
        self.stdout.write('📄 Checking Site Content...')
        for page_name, sections in PAGE_SECTIONS.items():
            for sec in sections:
                section_key = sec['section']
                field_type = sec.get('field', 'content')
                
                # Smart Content Generation
                dummy_title = f"{section_key.replace('_', ' ').title()} - XpertAI"
                dummy_content = (
                    f"This is placeholder content for {section_key}. "
                    "XpertAI Global delivers AI-driven financial solutions, "
                    "ensuring compliance, speed, and accuracy for your business."
                )

                defaults = {}
                if field_type == 'title':
                    defaults['title'] = dummy_title
                elif field_type == 'image':
                    pass # Images ko blank rehne dete hain
                else:
                    defaults['content'] = dummy_content

                obj, created = SiteContent.objects.get_or_create(
                    page=page_name,
                    section=section_key,
                    defaults=defaults
                )
                if created:
                    self.stdout.write(f"   ✅ Added: {page_name} -> {section_key}")

        # --- 2. SEED BLOGS ---
        if BlogPost.objects.count() == 0:
            self.stdout.write('📝 Seeding Blogs...')
            blogs = [
                {"title": "The Future of AI in Audit", "short_description": "How AI is transforming audits.", "body": "<p>AI is revolutionizing the audit industry...</p>"},
                {"title": "Tax Saving Strategies for 2025", "short_description": "Maximize your returns.", "body": "<p>Start planning your taxes early with these tips...</p>"},
                {"title": "Why Virtual CFOs are Essential", "short_description": "Scale your startup efficiently.", "body": "<p>A Virtual CFO brings expertise without the cost...</p>"},
            ]
            for b in blogs:
                BlogPost.objects.create(
                    title=b['title'], 
                    slug=b['title'].lower().replace(' ', '-'),
                    short_description=b['short_description'],
                    body=b['body'],
                    published=True
                )
                self.stdout.write(f"   ✅ Blog: {b['title']}")

        # --- 3. SEED CAREERS ---
        if JobOpening.objects.count() == 0:
            self.stdout.write('💼 Seeding Jobs...')
            jobs = [
                {"title": "Senior React Developer", "dept": "Tech", "loc": "Remote", "type": "Full-Time"},
                {"title": "Audit Manager", "dept": "Finance", "loc": "Delhi", "type": "Full-Time"},
                {"title": "Sales Executive", "dept": "Sales", "loc": "Mumbai", "type": "Part-Time"},
            ]
            for j in jobs:
                job = JobOpening.objects.create(
                    title=j['title'], department=j['dept'], location=j['loc'], type=j['type'],
                    description="Join our team to build the future of finance.", is_active=True
                )
                # Add a dummy application for this job
                JobApplication.objects.create(
                    job=job, applicant_name="Rahul Verma", email="rahul@example.com",
                    resume_link="https://linkedin.com/in/rahul", cover_letter="I am a great fit."
                )
                self.stdout.write(f"   ✅ Job: {j['title']}")

        # --- 4. SEED LEADS & CONTACTS ---
        if Lead.objects.count() == 0:
            self.stdout.write('👥 Seeding Leads...')
            Lead.objects.create(name="Amit Sharma", email="amit@test.com", service="Audit", message="Need audit for my firm.", source="website")
            Lead.objects.create(name="Priya Singh", email="priya@test.com", service="Tax", message="GST filing help.", source="chatbot")
            self.stdout.write("   ✅ Added Dummy Leads")

        if ContactMessage.objects.count() == 0:
            self.stdout.write('mb Seeding Messages...')
            ContactMessage.objects.create(name="John Doe", email="john@gmail.com", message="Hi, do you offer consulting?")
            self.stdout.write("   ✅ Added Contact Messages")

        if NewsletterSubscriber.objects.count() == 0:
            NewsletterSubscriber.objects.create(email="subscriber@demo.com")
            self.stdout.write("   ✅ Added Subscriber")

        # --- 5. SEED SERVICES, RESOURCES, CASE STUDIES ---
        if Service.objects.count() == 0:
            self.stdout.write('🛠 Seeding Services...')
            Service.objects.create(title="Virtual CFO", slug="virtual-cfo", short_description="Expert financial guidance.", full_description="<p>Detailed CFO services...</p>", icon="Briefcase")
            Service.objects.create(title="Taxation", slug="taxation", short_description="GST & ITR filing.", full_description="<p>Complete tax solutions...</p>", icon="FileText")
            self.stdout.write("   ✅ Added Services")

        if CaseStudy.objects.count() == 0:
            CaseStudy.objects.create(title="Startup Growth", client_name="TechNova", summary="Helped them scale.", result_stat="3x Revenue")
            self.stdout.write("   ✅ Added Case Study")

        if Resource.objects.count() == 0:
            Resource.objects.create(title="Financial Guide 2025", type="E-Book", description="Complete guide.")
            self.stdout.write("   ✅ Added Resource")

        # --- 6. SEED THEME ---
        if ThemeSetting.objects.count() == 0:
            ThemeSetting.objects.create(name="Default Corporate")
            self.stdout.write("   ✅ Added Default Theme")

        self.stdout.write(self.style.SUCCESS('🎉 DATABASE FULLY SEEDED! Website is ready.'))