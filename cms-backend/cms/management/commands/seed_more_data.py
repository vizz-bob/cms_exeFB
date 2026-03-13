from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from core.models import ExampleModel
from pages.models import PageContent
from cms.models import Page
from careers.models import JobOpening, JobApplication
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seeds extra data for Job Applications, Groups, Pages, and Example Models.'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Extra Data...')

        # --- 1. SEED DJANGO GROUPS ---
        groups = ['HR Manager', 'Content Editor', 'Lead Viewer', 'Super Admin']
        for g_name in groups:
            group, created = Group.objects.get_or_create(name=g_name)
            if created:
                self.stdout.write(f"   ✅ Group Created: {g_name}")
            else:
                self.stdout.write(f"   ℹ️ Group Exists: {g_name}")

        # --- 2. SEED EXAMPLE MODELS (Core App) ---
        if ExampleModel.objects.count() < 4:
            for i in range(1, 5):
                name = f"Example Item {i} - {random.randint(100, 999)}"
                ExampleModel.objects.create(name=name)
                self.stdout.write(f"   ✅ ExampleModel: {name}")

        # --- 3. SEED CMS PAGES (For Navbar) ---
        # Ye wo pages hain jo Navbar me dynamic aate hain
        cms_pages = [
            {"title": "Our Story", "slug": "our-story", "order": 1},
            {"title": "Team", "slug": "team", "order": 2},
            {"title": "FAQ", "slug": "faq", "order": 3},
            {"title": "Support", "slug": "support", "order": 4},
        ]
        for p in cms_pages:
            page, created = Page.objects.get_or_create(
                slug=p['slug'],
                defaults={'title': p['title'], 'page_order': p['order']}
            )
            if created:
                self.stdout.write(f"   ✅ CMS Page (Menu): {p['title']}")

        # --- 4. SEED PAGE CONTENT (For Static Pages) ---
        # Ye wo pages hain jo 'pages' app me text content hold karte hain (Terms, Privacy)
        content_pages = [
            {
                "slug": "terms-and-conditions", 
                "title": "Terms and Conditions", 
                "content": "<h2>Terms of Service</h2><p>Welcome to XpertAI Global. By using our services, you agree to...</p>"
            },
            {
                "slug": "privacy-policy", 
                "title": "Privacy Policy", 
                "content": "<h2>Privacy Policy</h2><p>We value your privacy. Your data is secure with us...</p>"
            },
            {
                "slug": "cookie-policy", 
                "title": "Cookie Policy", 
                "content": "<h2>Cookie Usage</h2><p>We use cookies to improve user experience...</p>"
            },
            {
                "slug": "refund-policy", 
                "title": "Refund Policy", 
                "content": "<h2>Refunds</h2><p>Refunds are processed within 7 working days...</p>"
            },
        ]
        for cp in content_pages:
            obj, created = PageContent.objects.get_or_create(
                slug=cp['slug'],
                defaults={'title': cp['title'], 'content': cp['content']}
            )
            if created:
                self.stdout.write(f"   ✅ Page Content: {cp['title']}")

        # --- 5. SEED JOB APPLICATIONS ---
        # Pehle check karte hain ki Jobs hain ya nahi, nahi to banayenge
        if JobOpening.objects.count() == 0:
            self.stdout.write("   ⚠️ No Jobs found! Creating dummy jobs first...")
            JobOpening.objects.create(title="Python Developer", department="Tech", type="Full-Time")
            JobOpening.objects.create(title="HR Executive", department="HR", type="Full-Time")
        
        jobs = JobOpening.objects.all()
        
        # Dummy Applicants Data
        applicants = [
            {"name": "Amit Verma", "email": "amit@example.com", "cover": "I have 3 years of experience."},
            {"name": "Sneha Gupta", "email": "sneha@example.com", "cover": "Looking for a challenging role."},
            {"name": "Rohan Das", "email": "rohan@example.com", "cover": "Expert in Django and React."},
            {"name": "Priya Sharma", "email": "priya@example.com", "cover": "HR professional with MBA."},
        ]

        for job in jobs:
            # Har job ke liye 2-3 applications daal dete hain
            if job.applications.count() < 4:
                for app_data in applicants:
                    JobApplication.objects.create(
                        job=job,
                        applicant_name=app_data['name'],
                        email=app_data['email'],
                        resume_link="https://linkedin.com/in/example",
                        cover_letter=f"Applying for {job.title}. {app_data['cover']}"
                    )
                    self.stdout.write(f"   ✅ Application: {app_data['name']} -> {job.title}")

        self.stdout.write(self.style.SUCCESS('🎉 EXTRA DATA SEEDED SUCCESSFULLY!'))