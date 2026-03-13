from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# --- IMPORTS ---
from cms.views import (
    SiteContentViewSet, 
    # home_page_content, # Removed if unused
    CaseStudyViewSet, 
    ResourceViewSet, 
    ServiceViewSet, 
    ServiceSubServiceViewSet,
    PageViewSet
)
from blog.views import BlogPostViewSet, BlogCategoryViewSet
from leads.views import LeadViewSet, NewsletterSubscriberViewSet, EmailTemplateViewSet, chat_flow_handler
from careers.views import JobOpeningViewSet, JobApplicationViewSet

# --- ROUTER REGISTRATION ---
router = DefaultRouter()

# CMS Endpoints
router.register(r'sitecontent', SiteContentViewSet)
router.register(r'case-studies', CaseStudyViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'sub-services', ServiceSubServiceViewSet)
router.register(r'pages', PageViewSet)

# Blog Endpoints
router.register(r'blogs', BlogPostViewSet, basename='blog')
router.register(r'blog-categories', BlogCategoryViewSet, basename='blog-category')

# Lead Endpoints
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'subscribers', NewsletterSubscriberViewSet)
router.register(r'email-templates', EmailTemplateViewSet)

# Career Endpoints 
# (Kept here to ensure /api/jobs/ works. If careers/urls.py also registers this, you can remove these lines)
router.register(r'jobs', JobOpeningViewSet)
router.register(r'apply', JobApplicationViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # --- AUTH & CORE ---
    path("", include("core.urls")), 

    # --- MAIN ROUTER (CMS, Blog, Leads, Careers) ---
    path("api/", include(router.urls)),
    
    # --- CUSTOM HANDLERS ---
    path("api/chatbot-flow/", chat_flow_handler),
    
    # --- THEME & BRANDING ---
    path("api/", include("theme.urls")),
    path("api/branding/", include("branding.urls")),
    
    # --- CUSTOM PAGES (Namespaced) ---
    path("api/", include("homepage.urls")),       
    path("api/about/", include("about.urls")), 
    path("api/", include("resources_page.urls")), 
    path("api/", include("lead_system_page.urls")), 
    path("api/legal/", include("legal.urls")),    
    path("api/", include("services_page.urls")),
    path("api/", include("careers.urls")),        # Ensure careers page data is loaded
    path("api/", include("stakeholders.urls")),   # Added Stakeholders
    
    # --- CONTACT APP (Dedicated Namespace) ---
    # This enables: api/contact/, api/contact/messages/, api/contact/tickets/
    path("api/contact/", include("contact.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)