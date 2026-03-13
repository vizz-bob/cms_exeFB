import csv
import zipfile
import io
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from .models import CareersPage, Benefit, JobOpening, JobApplication, EmployeeTestimonial

# --- Custom Admin Actions ---

def export_applications_csv(modeladmin, request, queryset):
    """
    Export selected applications to a CSV file.
    """
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]
    
    # Create the response object
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_applications.csv"'
    
    writer = csv.writer(response)
    # Write Header
    writer.writerow(field_names)
    
    # Write Data
    for obj in queryset:
        row = []
        for field in field_names:
            value = getattr(obj, field)
            if hasattr(value, 'url'): # Handle FileFields/ImageFields
                row.append(value.url)
            else:
                row.append(str(value))
        writer.writerow(row)
    
    return response

export_applications_csv.short_description = "Export Selected to CSV"

def download_resumes_zip(modeladmin, request, queryset):
    """
    Download resumes of selected applications as a ZIP file.
    """
    # Create a byte stream for the ZIP file
    zip_buffer = io.BytesIO()
    
    has_files = False
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for app in queryset:
            if app.resume_file:
                try:
                    # Construct a filename: ApplicantName_JobTitle_Resume.pdf
                    file_ext = app.resume_file.name.split('.')[-1]
                    filename = f"{app.applicant_name.replace(' ', '_')}_{app.job.title.replace(' ', '_')}.{file_ext}"
                    
                    # Read file content and write to zip
                    # Note: We use app.resume_file.open() to ensure we get the file handle
                    with app.resume_file.open('rb') as f:
                        zip_file.writestr(filename, f.read())
                    has_files = True
                except Exception as e:
                    # Handle missing files gracefully (e.g., if file was deleted from storage)
                    print(f"Error zipping file for {app.applicant_name}: {e}")
                    pass

    if not has_files:
        modeladmin.message_user(request, "No resume files found for selected applications.", level="WARNING")
        return

    # Prepare the response
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="resumes_bundle.zip"'
    return response

download_resumes_zip.short_description = "Download Resumes (ZIP)"

# --- Admin Registrations ---

@admin.register(CareersPage)
class CareersPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hero Section", {
            "fields": ("hero_title", "hero_subtitle")
        }),
        ("Content", {
            "fields": ("benefits_title", "benefits_subtitle", "culture_title", "culture_text", "culture_image", "openings_title")
        }),
        ("Form Labels & Requirements", {
            "fields": (
                "form_name_label", 
                "form_email_label", 
                "form_phone_label", "is_phone_required",
                "form_linkedin_label", "is_linkedin_required",
                "form_resume_label", 
                "form_cover_letter_label", "is_cover_letter_required"
            ),
            "description": "Customize the labels and mandatory status of form fields."
        }),
        ("Dynamic Field (Referral)", {
            "fields": (
                "show_referral_field", 
                "form_referral_label", 
                "is_referral_multiselect", 
                "referral_options"
            ),
            "description": "Configure the 'How did you hear about us?' section. Use comma-separated values for options."
        }),
    )

    def has_add_permission(self, request):
        return CareersPage.objects.count() == 0

@admin.register(Benefit)
class BenefitAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'icon_name', 'order')

@admin.register(EmployeeTestimonial)
class EmployeeTestimonialAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'role', 'order')

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'type', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('department', 'type', 'is_active')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'job', 'email', 'get_resume_download', 'referral_source', 'applied_at')
    list_filter = ('job', 'applied_at')
    search_fields = ('applicant_name', 'email', 'job__title')
    readonly_fields = ('applied_at',)
    
    # Add the custom actions
    actions = [export_applications_csv, download_resumes_zip]

    def get_resume_download(self, obj):
        """
        Provides a direct download link for the individual resume in the list view.
        """
        if obj.resume_file:
            return format_html('<a href="{}" download class="button" style="padding:4px 8px; background:#ddd; border-radius:4px; text-decoration:none;">Download PDF</a>', obj.resume_file.url)
        elif obj.resume_link:
             return format_html('<a href="{}" target="_blank" style="color:blue;">View Link</a>', obj.resume_link)
        return "-"
    
    get_resume_download.short_description = "Resume"
    get_resume_download.allow_tags = True