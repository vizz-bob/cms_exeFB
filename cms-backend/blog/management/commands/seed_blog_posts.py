from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import BlogCategory, BlogPost
import random

class Command(BaseCommand):
    help = 'Seeds the database with diverse Blog Categories and Posts for testing.'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding Blog Data...')

        # 1. Create Categories
        categories_data = [
            "Artificial Intelligence",
            "Financial Auditing",
            "Taxation Strategy",
            "Corporate News",
            "Regulatory Compliance",
            "Cloud Computing"
        ]
        
        categories = {}
        for cat_name in categories_data:
            cat, created = BlogCategory.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            categories[cat_name] = cat
            if created:
                self.stdout.write(f"   ✅ Created Category: {cat_name}")

        # 2. Create Blog Posts
        # We will create posts with specific keywords to test search (e.g., "AI", "Audit", "2025")
        blog_posts_data = [
            {
                "title": "The Rise of AI in Financial Auditing",
                "category": "Artificial Intelligence",
                "desc": "How machine learning algorithms are detecting fraud faster than ever.",
                "body": "<p>Deep dive into AI-driven audit trails...</p>"
            },
            {
                "title": "Tax Saving Strategies for FY 2025-2026",
                "category": "Taxation Strategy",
                "desc": "Essential tips for corporate tax planning in the new fiscal year.",
                "body": "<p>Understanding the new tax regime...</p>"
            },
            {
                "title": "Cloud Security for Fintech Companies",
                "category": "Cloud Computing",
                "desc": "Best practices for securing sensitive financial data on the cloud.",
                "body": "<p>Encryption and access control standards...</p>"
            },
            {
                "title": "XpertAI Expands to Europe",
                "category": "Corporate News",
                "desc": "Our journey continues with a new headquarters in London.",
                "body": "<p>We are thrilled to announce...</p>"
            },
            {
                "title": "Automating Regulatory Compliance Reports",
                "category": "Regulatory Compliance",
                "desc": "Stop doing manual compliance. Automate it with our new tool.",
                "body": "<p>Regulatory landscapes are changing...</p>"
            },
            {
                "title": "Machine Learning vs. Rule-Based Audits",
                "category": "Artificial Intelligence",
                "desc": "Why static rules are no longer enough for modern finance.",
                "body": "<p>Comparing the two approaches...</p>"
            },
            {
                "title": "5 Audit Mistakes to Avoid",
                "category": "Financial Auditing",
                "desc": "Common pitfalls that lead to compliance penalties.",
                "body": "<p>Checklist for internal auditors...</p>"
            },
            {
                "title": "The Future of Virtual CFOs",
                "category": "Financial Auditing",
                "desc": "How remote financial leadership is changing the startup ecosystem.",
                "body": "<p>Cost benefits and strategic advantages...</p>"
            }
        ]

        for post in blog_posts_data:
            # Generate unique slug
            base_slug = slugify(post['title'])
            unique_slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            cat_obj = categories.get(post['category'])
            
            obj, created = BlogPost.objects.get_or_create(
                title=post['title'],
                defaults={
                    "slug": unique_slug,
                    "category": cat_obj,
                    "short_description": post['desc'],
                    "body": post['body'],
                    "published": True,
                    "image": None # Optional: Add image path if you have one
                }
            )
            if created:
                self.stdout.write(f"   ✅ Created Post: {post['title']}")
            else:
                self.stdout.write(f"   ℹ️ Post Exists: {post['title']}")

        self.stdout.write(self.style.SUCCESS('🎉 Blog Data Seeded Successfully!'))