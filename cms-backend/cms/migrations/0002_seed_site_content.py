from django.db import migrations

HOME_CONTENT = [
    {"section": "hero_title", "title": "Empowering Global Businesses with Smart Financial Solutions"},
    {
        "section": "hero_text",
        "content": "XpertAI Global helps companies simplify accounting, auditing, taxation, and financial automation — backed by powerful AI-ready systems.",
    },
    {"section": "hero_image"},
    {"section": "services_title", "title": "Our Key Offerings"},
    {"section": "service1_title", "title": "Virtual CFO"},
    {"section": "service1_desc", "content": "End-to-end financial management and strategy."},
    {"section": "service2_title", "title": "Audit & Assurance"},
    {"section": "service2_desc", "content": "Accurate reports, compliance, and transparency."},
    {"section": "service3_title", "title": "Taxation Services"},
    {"section": "service3_desc", "content": "Smart GST, TDS, and ITR management systems."},
    {"section": "cta_title", "title": "Ready to Transform Your Financial Operations?"},
    {"section": "cta_button", "content": "Get in Touch"},
]

CONTACT_CONTENT = [
    {"section": "contact_header", "title": "Get in Touch"},
    {"section": "contact_subtext", "content": "We’re here to help you simplify finance with AI and automation."},
    {"section": "form_title", "title": "Send us a Message"},
    {"section": "info_title", "title": "Contact Information"},
    {
        "section": "info_text",
        "content": "Reach out to us for project collaboration, consultation, or financial services.",
    },
    {"section": "address", "content": "123 Corporate Avenue, Delhi, India"},
    {"section": "email", "content": "support@xpertai.global"},
    {"section": "phone", "content": "+91 98765 43210"},
    {"section": "map_link", "content": "https://maps.google.com"},
    {"section": "map_button", "title": "View Location"},
    {"section": "cta_title", "title": "Want to know how XpertAI can streamline your business?"},
    {"section": "cta_button", "content": "Visit CRM Portal →"},
]


def seed_site_content(apps, schema_editor):
    SiteContent = apps.get_model("cms", "SiteContent")

    defaults = {
        "home": HOME_CONTENT,
        "contact": CONTACT_CONTENT,
    }

    for page, entries in defaults.items():
        for entry in entries:
            SiteContent.objects.get_or_create(
                page=page,
                section=entry["section"],
                defaults={
                    "title": entry.get("title", ""),
                    "content": entry.get("content", ""),
                },
            )


def unseed_site_content(apps, schema_editor):
    SiteContent = apps.get_model("cms", "SiteContent")
    sections = [item["section"] for item in HOME_CONTENT + CONTACT_CONTENT]
    SiteContent.objects.filter(section__in=sections).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_site_content, unseed_site_content),
    ]

