from django.core.management.base import BaseCommand
from stakeholders.models import Stakeholder, SolutionsPage
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Seeds the Solutions Page content and Stakeholder cards with detailed data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Cleaning old Solutions data..."))
        
        # 1. Purana data delete karein taaki duplicate ya error na ho
        Stakeholder.objects.all().delete()
        SolutionsPage.objects.all().delete()

        # 2. Page Content Create karein
        SolutionsPage.objects.create(
            hero_title="Our Ecosystem",
            hero_subtitle="Connecting Clients, Experts, and Learners in one unified financial platform.",
            cta_title="Ready to find your place?",
            cta_text="Join XpertAI today. Whether you need service, want to work, or want to learn - we have a solution for you.",
            cta_btn_primary="Get Started",
            cta_btn_secondary="Contact Sales"
        )

        # 3. Detailed Solution Cards Data
        cards_data = [
            {
                "title": "Clients",
                "description": "Businesses and Startups seeking Virtual CFOs, Auditors, and Tax Experts.",
                "long_description": """
### **Empowering Businesses with Financial Intelligence**

As a Client on XpertAI, you get access to a vetted network of top-tier financial professionals. Whether you are a startup looking for a **Virtual CFO** or an enterprise needing **Audit & Compliance** services, our platform bridges the gap.

**What you get:**
* **On-Demand Experts:** Hire CAs, CS, and CMAs for specific projects or long-term roles.
* **AI-Driven Insights:** Our dashboard provides real-time financial health checks.
* **Secure Transactions:** All contracts and payments are secured via blockchain technology.
* **Compliance Automation:** Never miss a due date with our automated tax & compliance tracking.

Join us to streamline your financial operations and focus on what you do best—growing your business.
                """,
                "icon": "Building2",
                "order": 1
            },
            {
                "title": "Professionals",
                "description": "Chartered Accountants, CS, and CMAs looking for high-value projects.",
                "long_description": """
### **Grow Your Practice Globally**

Are you a Chartered Accountant, Company Secretary, or a Cost Accountant? XpertAI is your gateway to a global clientele. Move beyond geographical boundaries and find high-value consulting gigs.

**Why Join XpertAI?**
* **Verified Leads:** Stop chasing clients. Get matched with businesses that need your specific expertise.
* **Flexible Work:** Choose projects that fit your schedule—full-time, part-time, or hourly.
* **Smart Tools:** Use our built-in AI tools for faster audits, automated reporting, and tax filing.
* **Guaranteed Payment:** Our escrow system ensures you get paid for every milestone you deliver.

Elevate your professional career with the power of technology.
                """,
                "icon": "Briefcase",
                "order": 2
            },
            {
                "title": "Freelancers / Freshers",
                "description": "Emerging financial talent looking for internships and gig projects.",
                "long_description": """
### **Kickstart Your Financial Career**

For fresh graduates and emerging freelancers, the financial world can be tough to crack. XpertAI provides a launchpad for your career.

**Opportunities for You:**
* **Internships:** Find paid internships with top firms and startups.
* **Gig Projects:** Work on smaller tasks like bookkeeping, data entry, and reconciliation to build your portfolio.
* **Mentorship:** Connect with senior professionals who can guide your career path.
* **Skill Badges:** Earn verification badges by completing tasks and assessments on the platform.

Start your journey from a learner to a leader today.
                """,
                "icon": "GraduationCap",
                "order": 3
            },
            {
                "title": "Trainers",
                "description": "SMEs delivering specialized financial training and certifications.",
                "long_description": """
### **Monetize Your Knowledge**

If you are a Subject Matter Expert (SME) in finance, tax, or law, XpertAI offers you a platform to teach and train the next generation of professionals.

**How it works:**
* **Host Workshops:** Conduct live webinars or offline workshops for students and professionals.
* **Create Courses:** Upload your video courses on GST, Tally, Excel, or Valuation and earn royalties.
* **Corporate Training:** Get discovered by companies looking for corporate trainers for their finance teams.
* **Certification:** Issue blockchain-verified certificates to your students.

Share your wisdom and create a passive income stream.
                """,
                "icon": "Presentation",
                "order": 4
            },
            {
                "title": "Training Institutes",
                "description": "Educational organizations partnering for curriculum and placement.",
                "long_description": """
### **Partner for Excellence**

Training Institutes can leverage XpertAI to provide their students with practical exposure and placement opportunities.

**Partnership Benefits:**
* **Curriculum Support:** Align your syllabus with industry demands using our market insights.
* **Placement Assistance:** Direct access to our job portal for your passing-out batches.
* **Live Projects:** Give your students hands-on experience by assigning them real-world micro-projects managed by professionals.
* **Brand Visibility:** Showcase your institute to a network of corporates and professionals.

Let's work together to bridge the skill gap in the financial sector.
                """,
                "icon": "School",
                "order": 5
            }
        ]

        for card in cards_data:
            Stakeholder.objects.create(
                title=card["title"],
                # Slug automatic generate ho jayega model ke save method se
                description=card["description"],
                long_description=card["long_description"], # Ye naya data hai
                icon_name=card["icon"],
                order=card["order"]
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully populated Solutions Page with {len(cards_data)} detailed cards!"))