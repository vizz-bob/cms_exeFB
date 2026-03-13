from django.core.management.base import BaseCommand
from careers.models import CareersPage, Benefit, JobOpening, EmployeeTestimonial

class Command(BaseCommand):
    help = 'Seeds Careers Page according to Document 2'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Careers Full Data...')

        # 1. Page Content
        CareersPage.objects.update_or_create(id=1, defaults={
            "hero_title": "Join the Revolution",
            "hero_subtitle": "We are building the operating system for the future of finance. Come build with us.",
            "benefits_title": "Perks & Benefits",
            "culture_text": "Our culture is built on transparency, autonomy, and a relentless pursuit of excellence. We don't micromanage; we empower.",
            "openings_title": "Open Positions"
        })

        # 2. Benefits
        benefits = [
            {"title": "Global Exposure", "description": "Work with Fortune 500 clients.", "icon_name": "Globe", "order": 1},
            {"title": "Top Compensation", "description": "Competitive salary + equity.", "icon_name": "DollarSign", "order": 2},
            {"title": "Remote First", "description": "Work from anywhere.", "icon_name": "Laptop", "order": 3},
            {"title": "Health & Wellness", "description": "Premium insurance for you & family.", "icon_name": "Heart", "order": 4},
        ]
        Benefit.objects.all().delete()
        for b in benefits:
            Benefit.objects.create(**b)

        # 3. Employee Testimonials
        testimonials = [
            {"name": "Rahul Sharma", "role": "Senior Engineer", "quote": "The autonomy here is unmatched. I shipped a core feature in my first week.", "order": 1},
            {"name": "Priya Patel", "role": "Product Designer", "quote": "A culture that truly values creativity and data-driven design.", "order": 2},
        ]
        EmployeeTestimonial.objects.all().delete()
        for t in testimonials:
            EmployeeTestimonial.objects.create(**t)

        # 4. Jobs & Internships
        jobs = [
            # Full Time Jobs
            {"title": "Senior Backend Engineer", "department": "Engineering", "location": "Remote", "type": "Full-Time", "description": "Python/Django expert needed."},
            {"title": "Tax Consultant", "department": "Finance", "location": "Mumbai", "type": "Full-Time", "description": "Expert in GST and International Tax."},
            
            # Internships (Crucial for Doc 2)
            {"title": "Finance Intern", "department": "Finance", "location": "Bangalore", "type": "Internship", "description": "Assist with audit preparations and tax filings. 6-month stipend based."},
            {"title": "AI Research Intern", "department": "Engineering", "location": "Remote", "type": "Internship", "description": "Work on LLM fine-tuning for financial data."},
        ]
        JobOpening.objects.all().delete()
        for j in jobs:
            JobOpening.objects.create(**j)

        self.stdout.write(self.style.SUCCESS('🎉 Careers Page Fully Seeded!'))