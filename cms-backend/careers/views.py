import csv
import zipfile
import io
from django.http import HttpResponse, FileResponse # <--- Import FileResponse
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CareersPage, Benefit, JobOpening, JobApplication, EmployeeTestimonial
from .serializers import (
    CareersPageSerializer, BenefitSerializer, 
    JobOpeningSerializer, JobApplicationSerializer, EmployeeTestimonialSerializer
)

# --- 1. Public Data View (Read Only) ---
class CareersPageDataView(APIView):
    def get(self, request):
        content, created = CareersPage.objects.get_or_create(id=1)
        return Response({
            "content": CareersPageSerializer(content).data,
            "benefits": BenefitSerializer(Benefit.objects.all(), many=True).data,
            "testimonials": EmployeeTestimonialSerializer(EmployeeTestimonial.objects.all(), many=True).data,
            "jobs": JobOpeningSerializer(JobOpening.objects.filter(is_active=True).order_by('-created_at'), many=True).data
        })

# --- 2. Admin CRUD ViewSets ---

class CareersPageViewSet(viewsets.ModelViewSet):
    queryset = CareersPage.objects.all()
    serializer_class = CareersPageSerializer

class BenefitViewSet(viewsets.ModelViewSet):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer

class EmployeeTestimonialViewSet(viewsets.ModelViewSet):
    queryset = EmployeeTestimonial.objects.all()
    serializer_class = EmployeeTestimonialSerializer

class JobOpeningViewSet(viewsets.ModelViewSet):
    queryset = JobOpening.objects.all().order_by('-created_at')
    serializer_class = JobOpeningSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all().order_by('-applied_at')
    serializer_class = JobApplicationSerializer

    # --- Helper: Generate CSV ---
    def _generate_csv(self, queryset):
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        meta = self.queryset.model._meta
        field_names = [field.name for field in meta.fields]
        writer.writerow(field_names)
        for obj in queryset:
            row = []
            for field in field_names:
                value = getattr(obj, field)
                if hasattr(value, 'url'):
                    row.append(value.url)
                else:
                    row.append(str(value))
            writer.writerow(row)
        return buffer.getvalue()

    # --- Helper: Generate ZIP ---
    def _generate_zip(self, queryset):
        zip_buffer = io.BytesIO()
        has_files = False
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for app in queryset:
                if app.resume_file:
                    try:
                        ext = app.resume_file.name.split('.')[-1]
                        filename = f"{app.applicant_name.replace(' ', '_')}_{app.job.title.replace(' ', '_')}_{app.id}.{ext}"
                        with app.resume_file.open('rb') as f:
                            zip_file.writestr(filename, f.read())
                        has_files = True
                    except Exception:
                        pass
        zip_buffer.seek(0)
        return zip_buffer.getvalue() if has_files else None

    # --- ACTION: Export All to CSV ---
    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        csv_data = self._generate_csv(self.queryset)
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applications_export.csv"'
        return response

    # --- ACTION: Export Single Detail to CSV ---
    @action(detail=True, methods=['get'])
    def download_details(self, request, pk=None):
        obj = self.get_object()
        csv_data = self._generate_csv([obj])
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="application_{pk}_details.csv"'
        return response

    # --- ACTION: Download Single Resume (New) ---
    @action(detail=True, methods=['get'])
    def download_resume(self, request, pk=None):
        """
        Forces the browser to download the resume file.
        """
        application = self.get_object()
        if not application.resume_file:
            return Response({'error': 'No resume file attached.'}, status=404)
        
        try:
            # Open file in binary read mode
            file_handle = application.resume_file.open('rb')
            response = FileResponse(file_handle, content_type='application/pdf')
            
            # Clean filename for download
            filename = f"{application.applicant_name.replace(' ', '_')}_Resume.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except FileNotFoundError:
            return Response({'error': 'File not found on server.'}, status=404)

    # --- ACTION: Download Bulk Resumes (ZIP) ---
    @action(detail=False, methods=['get'])
    def download_resumes(self, request):
        zip_data = self._generate_zip(self.queryset)
        if not zip_data:
            return Response({"error": "No resume files found."}, status=404)
        response = HttpResponse(zip_data, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="resumes_bulk.zip"'
        return response

    # --- ACTION: Share via Email ---
    @action(detail=False, methods=['post'])
    def share_via_email(self, request):
        target_email = request.data.get('email')
        share_type = request.data.get('type')
        obj_id = request.data.get('id')
        
        if not target_email:
            return Response({"error": "Email is required"}, status=400)

        subject = "Shared Careers Data"
        body = "Please find the requested data attached."
        
        email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [target_email])

        try:
            if share_type == 'csv_all':
                email.subject = "Bulk Applications Export (CSV)"
                csv_content = self._generate_csv(self.queryset)
                email.attach("applications_bulk.csv", csv_content, 'text/csv')

            elif share_type == 'zip_resumes':
                email.subject = "Bulk Resumes Export (ZIP)"
                zip_content = self._generate_zip(self.queryset)
                if not zip_content:
                     return Response({"error": "No resumes available to zip."}, status=400)
                email.attach("resumes_bulk.zip", zip_content, 'application/zip')

            elif share_type == 'csv_single' and obj_id:
                obj = JobApplication.objects.get(id=obj_id)
                email.subject = f"Application: {obj.applicant_name} - {obj.job.title}"
                email.body = f"Application details for {obj.applicant_name} attached."
                
                if obj.resume_file:
                    try:
                        file_name = obj.resume_file.name.split('/')[-1]
                        with obj.resume_file.open('rb') as f:
                            pdf_content = f.read()
                        email.attach(file_name, pdf_content, 'application/pdf')
                    except Exception as e:
                        email.body += f"\n\n[Warning: Could not attach resume file. Error: {str(e)}]"
            else:
                return Response({"error": "Invalid request"}, status=400)

            email.send()
            return Response({"success": True, "message": f"Email sent to {target_email}"})

        except Exception as e:
            return Response({"error": str(e)}, status=500)