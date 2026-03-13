from django.db import migrations

ABOUT_CONTENT = [
    {"section": "hero_title", "title": "About XpertAI Global"},
    {
        "section": "hero_text",
        "content": (
            "XpertAI Global is a next-generation financial consultancy firm dedicated to helping organizations "
            "modernize their accounting, audit, and business intelligence systems through cutting-edge automation."
        ),
    },
    {"section": "mission_title", "title": "Our Mission"},
    {
        "section": "mission_text",
        "content": "To simplify and digitize global finance using intelligent solutions that empower businesses to thrive.",
    },
    {"section": "vision_title", "title": "Our Vision"},
    {
        "section": "vision_text",
        "content": "To become a global leader in AI-driven financial consulting by transforming the way organizations manage money.",
    },
    {"section": "values_title", "title": "Our Values"},
    {
        "section": "values_text",
        "content": "Integrity, Innovation, and Impact — the pillars that drive every engagement at XpertAI Global.",
    },
    {"section": "cta_title", "title": "Our Journey Continues"},
    {"section": "cta_text", "content": "Let’s shape the future of digital finance — together."},
]

SERVICES_CONTENT = [
    {"section": "hero_title", "title": "Our Services"},
    {
        "section": "hero_text",
        "content": (
            "At XpertAI Global, we deliver tailored solutions that combine financial expertise with intelligent systems — "
            "empowering companies to stay ahead in a data-driven world."
        ),
    },
]

SERVICE_CARD_DATA = [
    ("Virtual CFO", "Get a dedicated financial expert to oversee strategy, forecasting, and performance."),
    ("Audit & Assurance", "Comprehensive audits to ensure compliance, transparency, and trust."),
    ("Taxation Advisory", "Optimize GST, TDS, and corporate tax management with simplified workflows."),
    ("Payroll & Compliance", "Manage payrolls, PF, and compliance reports through automated systems."),
    ("Financial Analytics", "Access real-time dashboards and data-driven insights for confident decisions."),
    ("Business Valuation", "Determine accurate valuations for funding, mergers, or acquisitions."),
]

SERVICES_CONTENT.extend(
    [
        {"section": f"service_card_{idx}_title", "title": title}
        for idx, (title, _) in enumerate(SERVICE_CARD_DATA, start=1)
    ]
    + [
        {"section": f"service_card_{idx}_desc", "content": desc}
        for idx, (_, desc) in enumerate(SERVICE_CARD_DATA, start=1)
    ]
)

SERVICES_CONTENT.extend(
    [
        {"section": "cta_title", "title": "Looking for a Custom Financial Solution?"},
        {
            "section": "cta_text",
            "content": "Our experts are ready to help you design, deploy, and optimize your finance strategy.",
        },
        {"section": "cta_button", "content": "Contact Us"},
    ]
)

FEATURE_CARD_DATA = [
    ("AI-Powered Financial Automation", "Automate invoices, reconciliation, and forecasting with AI workflows."),
    ("Real-Time Dashboards", "Monitor KPIs, revenue streams, and risk insights with dynamic visualizations."),
    ("Audit & Assurance Engine", "Create audit trails and ensure compliance through intelligent analytics."),
    ("Document Management", "Securely manage contracts, invoices, and reports with version control."),
    ("User Roles & Permissions", "Custom access levels for Admin, Credit, Legal, and Compliance teams."),
    ("Cloud-Ready & Scalable", "Deploy on scalable cloud infrastructure with real-time sync."),
]

FEATURES_CONTENT = [
    {"section": "hero_title", "title": "Our Core Features"},
    {
        "section": "hero_text",
        "content": "Discover how XpertAI Global integrates intelligence, analytics, and automation into financial management.",
    },
]
FEATURES_CONTENT.extend(
    [
        {"section": f"feature_card_{idx}_title", "title": title}
        for idx, (title, _) in enumerate(FEATURE_CARD_DATA, start=1)
    ]
    + [
        {"section": f"feature_card_{idx}_desc", "content": desc}
        for idx, (_, desc) in enumerate(FEATURE_CARD_DATA, start=1)
    ]
)

STAKEHOLDER_CARD_DATA = [
    ("CRM & Sales Team", "Manage leads, follow-ups, and relationships with built-in AI tracking.", "📞"),
    ("Credit & Finance Team", "Automate credit scoring, approvals, and reconciliation.", "💰"),
    ("Legal & Compliance Team", "Ensure documentation accuracy and audit readiness with secure records.", "⚖️"),
    ("Field & Verification Team", "Track verification activities and inspection reports in real-time.", "📋"),
    ("Audit & Risk Team", "Run internal audits and risk evaluations with automated analytics.", "📊"),
    ("Admin & Management", "Oversee modules, permissions, and unified business dashboards.", "🧭"),
]

STAKEHOLDER_CONTENT = [
    {"section": "hero_title", "title": "Stakeholder Ecosystem"},
    {
        "section": "hero_text",
        "content": "One unified platform that enables collaboration, automation, and visibility across departments.",
    },
]

STAKEHOLDER_CONTENT.extend(
    [
        {"section": f"stakeholder_card_{idx}_title", "title": title}
        for idx, (title, _, _) in enumerate(STAKEHOLDER_CARD_DATA, start=1)
    ]
    + [
        {"section": f"stakeholder_card_{idx}_desc", "content": desc}
        for idx, (_, desc, _) in enumerate(STAKEHOLDER_CARD_DATA, start=1)
    ]
    + [
        {"section": f"stakeholder_card_{idx}_icon", "content": icon}
        for idx, (_, _, icon) in enumerate(STAKEHOLDER_CARD_DATA, start=1)
    ]
)

RESOURCES_CONTENT = [
    {"section": "hero_title", "title": "Resources & Knowledge Center"},
    {
        "section": "hero_text",
        "content": "Explore whitepapers, research insights, and case studies by XpertAI Global.",
    },
    {"section": "downloads_title", "title": "Downloads & Case Studies"},
    {"section": "blog_highlight_title", "title": "From Our Blog"},
]

RESOURCE_CARD_DATA = [
    (
        "AI in Financial Auditing - Whitepaper",
        "Learn how AI transforms audits with accuracy and speed.",
        "#",
    ),
    (
        "Digital CFO Playbook 2025",
        "A guide to implementing digital transformation in finance.",
        "#",
    ),
    (
        "Automation in Compliance Management",
        "See how automation reduces manual errors and ensures compliance.",
        "#",
    ),
]

RESOURCES_CONTENT.extend(
    [
        {"section": f"resource_card_{idx}_title", "title": title}
        for idx, (title, _, _) in enumerate(RESOURCE_CARD_DATA, start=1)
    ]
    + [
        {"section": f"resource_card_{idx}_desc", "content": desc}
        for idx, (_, desc, _) in enumerate(RESOURCE_CARD_DATA, start=1)
    ]
    + [
        {"section": f"resource_card_{idx}_link", "content": link}
        for idx, (_, _, link) in enumerate(RESOURCE_CARD_DATA, start=1)
    ]
)

LEAD_SYSTEM_CONTENT = [
    {"section": "hero_title", "title": "Lead Generation Portal"},
    {
        "section": "hero_text",
        "content": "Capture potential client leads, inquiries, and partnership requests through the CRM engine.",
    },
    {"section": "cta_title", "title": "Track. Convert. Grow."},
    {"section": "cta_text", "content": "All your client leads — centralized in one CRM dashboard."},
]

CAREERS_CONTENT = [
    {"section": "hero_title", "title": "Join Our Team"},
    {
        "section": "hero_text",
        "content": "Be part of XpertAI Global’s mission to revolutionize financial technology.",
    },
    {"section": "openings_title", "title": "Current Openings"},
    {"section": "form_title", "title": "Submit Your Application"},
    {"section": "form_subtext", "content": "Share your profile and we will reach out for the best-fit role."},
]

JOB_CARD_DATA = [
    ("Frontend Developer", "Technology", "Remote", "Full-Time"),
    ("Financial Analyst", "Finance", "Delhi, India", "Full-Time"),
    ("AI Research Intern", "Data Science", "Remote", "Internship"),
]

CAREERS_CONTENT.extend(
    [
        {"section": f"job_card_{idx}_title", "title": title}
        for idx, (title, _, _, _) in enumerate(JOB_CARD_DATA, start=1)
    ]
    + [
        {"section": f"job_card_{idx}_dept", "content": dept}
        for idx, (_, dept, _, _) in enumerate(JOB_CARD_DATA, start=1)
    ]
    + [
        {"section": f"job_card_{idx}_location", "content": location}
        for idx, (_, _, location, _) in enumerate(JOB_CARD_DATA, start=1)
    ]
    + [
        {"section": f"job_card_{idx}_type", "content": job_type}
        for idx, (_, _, _, job_type) in enumerate(JOB_CARD_DATA, start=1)
    ]
)

BLOG_CONTENT = [
    {"section": "hero_title", "title": "Insights & Articles"},
    {
        "section": "hero_text",
        "content": "Stay ahead with expert insights, best practices, and innovations from XpertAI Global.",
    },
]


PAGE_DEFAULTS = {
    "about": ABOUT_CONTENT,
    "services": SERVICES_CONTENT,
    "features": FEATURES_CONTENT,
    "stakeholders": STAKEHOLDER_CONTENT,
    "resources": RESOURCES_CONTENT,
    "lead_system": LEAD_SYSTEM_CONTENT,
    "careers": CAREERS_CONTENT,
    "blog": BLOG_CONTENT,
}


def seed_additional_content(apps, schema_editor):
    SiteContent = apps.get_model("cms", "SiteContent")
    for page, entries in PAGE_DEFAULTS.items():
        for entry in entries:
            SiteContent.objects.get_or_create(
                page=page,
                section=entry["section"],
                defaults={
                    "title": entry.get("title", ""),
                    "content": entry.get("content", ""),
                },
            )


def unseed_additional_content(apps, schema_editor):
    SiteContent = apps.get_model("cms", "SiteContent")
    sections = [entry["section"] for entries in PAGE_DEFAULTS.values() for entry in entries]
    SiteContent.objects.filter(section__in=sections).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0002_seed_site_content"),
    ]

    operations = [
        migrations.RunPython(seed_additional_content, unseed_additional_content),
    ]

