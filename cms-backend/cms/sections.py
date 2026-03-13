def _card_sections(prefix, count, label_prefix):
    sections = []
    for idx in range(1, count + 1):
        sections.append(
            {
                "section": f"{prefix}_{idx}_title",
                "label": f"{label_prefix} {idx} • Title",
                "field": "title",
            }
        )
        sections.append(
            {
                "section": f"{prefix}_{idx}_desc",
                "label": f"{label_prefix} {idx} • Description",
                "field": "content",
            }
        )
    return sections


def _resource_sections(count):
    sections = []
    for idx in range(1, count + 1):
        sections.extend(
            [
                {
                    "section": f"resource_card_{idx}_title",
                    "label": f"Resource {idx} • Title",
                    "field": "title",
                },
                {
                    "section": f"resource_card_{idx}_desc",
                    "label": f"Resource {idx} • Description",
                    "field": "content",
                },
                {
                    "section": f"resource_card_{idx}_link",
                    "label": f"Resource {idx} • Link URL",
                    "field": "content",
                },
            ]
        )
    return sections


def _stakeholder_sections(count):
    sections = []
    for idx in range(1, count + 1):
        sections.extend(
            [
                {
                    "section": f"stakeholder_card_{idx}_title",
                    "label": f"Stakeholder Card {idx} • Title",
                    "field": "title",
                },
                {
                    "section": f"stakeholder_card_{idx}_desc",
                    "label": f"Stakeholder Card {idx} • Description",
                    "field": "content",
                },
                {
                    "section": f"stakeholder_card_{idx}_icon",
                    "label": f"Stakeholder Card {idx} • Icon/Emoji",
                    "field": "content",
                },
            ]
        )
    return sections


def _job_sections(count):
    sections = []
    for idx in range(1, count + 1):
        sections.extend(
            [
                {
                    "section": f"job_card_{idx}_title",
                    "label": f"Job Card {idx} • Role Title",
                    "field": "title",
                },
                {
                    "section": f"job_card_{idx}_dept",
                    "label": f"Job Card {idx} • Department",
                    "field": "content",
                },
                {
                    "section": f"job_card_{idx}_location",
                    "label": f"Job Card {idx} • Location",
                    "field": "content",
                },
                {
                    "section": f"job_card_{idx}_type",
                    "label": f"Job Card {idx} • Type",
                    "field": "content",
                },
            ]
        )
    return sections


PAGE_SECTIONS = {
    # --- UPDATED HOME PAGE CONFIGURATION ---
    "home": [
        # Hero Section
        {"section": "hero_title", "label": "Hero • Title", "field": "title"},
        {"section": "hero_text", "label": "Hero • Subtitle", "field": "content"},
        {"section": "hero_image", "label": "Hero • Image", "field": "image"},
        {"section": "cta_button", "label": "Hero • CTA Button", "field": "content"},

        # Stats Section (New)
        {"section": "stat1_label", "label": "Stat 1 • Label", "field": "title"},
        {"section": "stat1_value", "label": "Stat 1 • Value", "field": "title"},
        {"section": "stat2_label", "label": "Stat 2 • Label", "field": "title"},
        {"section": "stat2_value", "label": "Stat 2 • Value", "field": "title"},
        {"section": "stat3_label", "label": "Stat 3 • Label", "field": "title"},
        {"section": "stat3_value", "label": "Stat 3 • Value", "field": "title"},

        # Services Preview
        {"section": "services_title", "label": "Services • Title", "field": "title"},
        {"section": "service1_title", "label": "Service 1 • Title", "field": "title"},
        {"section": "service1_desc", "label": "Service 1 • Description", "field": "content"},
        {"section": "service2_title", "label": "Service 2 • Title", "field": "title"},
        {"section": "service2_desc", "label": "Service 2 • Description", "field": "content"},
        {"section": "service3_title", "label": "Service 3 • Title", "field": "title"},
        {"section": "service3_desc", "label": "Service 3 • Description", "field": "content"},

        # Features Section
        {"section": "features_title", "label": "Features • Title", "field": "title"},
        {"section": "feature1_title", "label": "Feature 1 • Title", "field": "title"},
        {"section": "feature1_desc", "label": "Feature 1 • Desc", "field": "content"},
        {"section": "feature2_title", "label": "Feature 2 • Title", "field": "title"},
        {"section": "feature2_desc", "label": "Feature 2 • Desc", "field": "content"},
        {"section": "feature3_title", "label": "Feature 3 • Title", "field": "title"},
        {"section": "feature3_desc", "label": "Feature 3 • Desc", "field": "content"},

        # Testimonials
        {"section": "testimonials_title", "label": "Testimonials • Title", "field": "title"},
        {"section": "testimonial1_text", "label": "Testimonial 1 • Quote", "field": "content"},
        {"section": "testimonial1_author", "label": "Testimonial 1 • Author", "field": "title"},
        {"section": "testimonial2_text", "label": "Testimonial 2 • Quote", "field": "content"},
        {"section": "testimonial2_author", "label": "Testimonial 2 • Author", "field": "title"},
        {"section": "testimonial3_text", "label": "Testimonial 3 • Quote", "field": "content"},
        {"section": "testimonial3_author", "label": "Testimonial 3 • Author", "field": "title"},

        # Bottom CTA
        {"section": "cta_title", "label": "Bottom CTA • Title", "field": "title"},
        {"section": "cta_text", "label": "Bottom CTA • Text", "field": "content"},
        {"section": "cta_button_text", "label": "Bottom CTA • Button", "field": "title"},
    ],

    # --- CONTACT PAGE ---
    "contact": [
        {"section": "contact_header", "label": "Hero • Title", "field": "title"},
        {"section": "contact_subtext", "label": "Hero • Subtitle", "field": "content"},
        
        # Form Controls
        {"section": "form_title", "label": "Form • Title", "field": "title"},
        {"section": "form_subtext", "label": "Form • Helper Text", "field": "content"},
        {"section": "form_button_text", "label": "Form • Button Label", "field": "title"},
        {"section": "form_success_msg", "label": "Form • Success Message", "field": "content"},
        
        # Info Panel
        {"section": "info_title", "label": "Info Panel • Title", "field": "title"},
        {"section": "info_text", "label": "Info Panel • Description", "field": "content"},
        {"section": "address", "label": "Info Panel • Address", "field": "content"},
        {"section": "email", "label": "Info Panel • Email", "field": "content"},
        {"section": "phone", "label": "Info Panel • Phone", "field": "content"},
        {"section": "map_link", "label": "Info Panel • Map Embed URL", "field": "content"},
        {"section": "map_button", "label": "Info Panel • Map Button", "field": "title"},
        {"section": "cta_title", "label": "CTA • Title", "field": "title"},
        {"section": "cta_button", "label": "CTA • Button Text", "field": "content"},
    ],

    # --- ABOUT PAGE ---
    "about": [
        {"section": "hero_title", "label": "Hero • Title", "field": "title"},
        {"section": "hero_text", "label": "Hero • Subtitle", "field": "content"},
        {"section": "mission_title", "label": "Mission • Title", "field": "title"},
        {"section": "mission_text", "label": "Mission • Description", "field": "content"},
        {"section": "vision_title", "label": "Vision • Title", "field": "title"},
        {"section": "vision_text", "label": "Vision • Description", "field": "content"},
        {"section": "values_title", "label": "Values • Title", "field": "title"},
        {"section": "values_text", "label": "Values • Description", "field": "content"},
        {"section": "cta_title", "label": "CTA • Title", "field": "title"},
        {"section": "cta_text", "label": "CTA • Description", "field": "content"},
    ],

    # --- SERVICES PAGE ---
    "services": [
        {"section": "hero_title", "label": "Hero • Title", "field": "title"},
        {"section": "hero_text", "label": "Hero • Subtitle", "field": "content"},
        *_card_sections("service_card", 6, "Service Card"),
        {"section": "cta_title", "label": "CTA • Title", "field": "title"},
        {"section": "cta_text", "label": "CTA • Description", "field": "content"},
        {"section": "cta_button", "label": "CTA • Button Text", "field": "content"},
    ],

    # --- FEATURES PAGE ---
    "features": [
        {"section": "hero_title", "label": "Hero • Title", "field": "title"},
        {"section": "hero_text", "label": "Hero • Subtitle", "field": "content"},
        *_card_sections("feature_card", 6, "Feature Card"),
    ],

    # --- STAKEHOLDERS PAGE ---
    "stakeholders": [
        {"section": "hero_title", "label": "Hero • Title", "field": "title"},
        {"section": "hero_text", "label": "Hero • Subtitle", "field": "content"},
        *_stakeholder_sections(6),
    ],

    # --- RESOURCES PAGE ---
    "resources": [
        {"section": "hero_title", "label": "Hero • Title", "field": "title"},
        {"section": "hero_text", "label": "Hero • Subtitle", "field": "content"},
        {"section": "downloads_title", "label": "Downloads • Section Title", "field": "title"},
        *_resource_sections(3),
        {"section": "blog_highlight_title", "label": "Blog Highlight • Title", "field": "title"},
    ],

    # --- LEAD SYSTEM PAGE ---
    "lead_system": [
        {"section": "hero_title", "label": "Hero • Title", "field": "title"},
        {"section": "hero_text", "label": "Hero • Subtitle", "field": "content"},
        {"section": "cta_title", "label": "CTA • Title", "field": "title"},
        {"section": "cta_text", "label": "CTA • Description", "field": "content"},
    ],

    # --- CAREERS PAGE ---
    "careers": [
        {"section": "hero_title", "label": "Hero • Title", "field": "title"},
        {"section": "hero_text", "label": "Hero • Subtitle", "field": "content"},
        {"section": "openings_title", "label": "Openings • Section Title", "field": "title"},
        *_job_sections(3),
        {"section": "form_title", "label": "Form • Title", "field": "title"},
        {"section": "form_subtext", "label": "Form • Description", "field": "content"},
        {"section": "form_button_text", "label": "Form • Button Label", "field": "title"},
        {"section": "form_success_msg", "label": "Form • Success Message", "field": "content"},
    ],

    # --- BLOG PAGE ---
    "blog": [
        # Hero Section
        {"section": "hero_title", "label": "Hero • Title", "field": "title"},
        {"section": "hero_text", "label": "Hero • Subtitle", "field": "content"},
        
        # Sidebar & Grid Section Labels
        {"section": "category_title", "label": "Sidebar • Filter Title", "field": "title"},
        {"section": "search_placeholder", "label": "Sidebar • Search Header", "field": "title"},
        {"section": "latest_posts_title", "label": "Main Area • Posts Title", "field": "title"},
    ],

    # --- FOOTER SECTION ---
    "footer": [
        {"section": "copyright_text", "label": "Copyright • Text", "field": "content"},
        {"section": "social_links_title", "label": "Socials • Title", "field": "title"},
        {"section": "facebook_url", "label": "Socials • Facebook URL", "field": "content"},
        {"section": "linkedin_url", "label": "Socials • LinkedIn URL", "field": "content"},
        {"section": "twitter_url", "label": "Socials • X (Twitter) URL", "field": "content"},
        {"section": "instagram_url", "label": "Socials • Instagram URL", "field": "content"},
        {"section": "contact_column_title", "label": "Contact Column • Title", "field": "title"},
        {"section": "contact_email", "label": "Contact Column • Email", "field": "content"},
        {"section": "contact_phone", "label": "Contact Column • Phone", "field": "content"},
        {"section": "links_column_title", "label": "Links Column • Title", "field": "title"},
    ],

    # --- LEAD SYSTEM PAGE (UPDATED) ---
    "lead_system": [
        {"section": "hero_title", "label": "Hero • Title", "field": "title"},
        {"section": "hero_text", "label": "Hero • Subtitle", "field": "content"},

        # --- NEW: DASHBOARD PREVIEW SECTION ---
        {"section": "dashboard_image", "label": "Dashboard • Image (Optional)", "field": "image"},
        {"section": "dashboard_text", "label": "Dashboard • Placeholder Text", "field": "content"},
        
        # New Feature Cards for Lead System
        *_card_sections("ls_feature", 3, "Feature"),
        
        {"section": "cta_title", "label": "CTA • Title", "field": "title"},
        {"section": "cta_text", "label": "CTA • Description", "field": "content"},
        {"section": "cta_button", "label": "CTA • Button Text", "field": "title"},
    ]
}


def get_section_slugs(page):
    """Return the list of allowed section identifiers for a page."""
    return [entry["section"] for entry in PAGE_SECTIONS.get(page, [])]


def get_help_text():
    """Return a readable help string for the admin form."""
    lines = []
    for page, entries in PAGE_SECTIONS.items():
        sections = ", ".join(entry["section"] for entry in entries)
        lines.append(f"{page.capitalize()}: {sections}")
    return "Available sections per page → " + " | ".join(lines)