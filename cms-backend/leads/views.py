from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.mail import send_mass_mail
from theme.models import ChatbotFlowStep
from .models import Lead, NewsletterSubscriber, LeadShareHistory, EmailTemplate
from .serializers import LeadSerializer, NewsletterSubscriberSerializer, LeadShareHistorySerializer, EmailTemplateSerializer
import logging
import os

logger = logging.getLogger(__name__)

# --- 1. Lead ViewSet ---
class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by("-created_at")
    serializer_class = LeadSerializer

    # --- Upload CSV for Sharing ---
    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        file_name = f"exports/{file_obj.name}"
        path = default_storage.save(file_name, ContentFile(file_obj.read()))
        
        if settings.MEDIA_URL.startswith("http"):
             file_url = f"{settings.MEDIA_URL}{path}"
        else:
             file_url = request.build_absolute_uri(settings.MEDIA_URL + path)

        return Response({"url": file_url}, status=status.HTTP_201_CREATED)

    # --- Share Lead API (FIXED KEYERROR) ---
    @action(detail=True, methods=['post'], url_path='share')
    def share_lead(self, request, pk=None):
        lead = self.get_object()
        recipients = request.data.get('recipients', [])
        
        # Fallback for single entry (legacy support)
        if not recipients:
            name = request.data.get('recipient_name') or request.data.get('name')
            phone = request.data.get('recipient_phone') or request.data.get('phone')
            if name and phone:
                recipients = [{'name': name, 'phone': phone}]

        if not recipients:
            return Response({"error": "No recipients provided."}, status=status.HTTP_400_BAD_REQUEST)

        created_records = []
        for r in recipients:
            # FIX: Handle both 'name' (from form) and 'recipient_name' (from history)
            r_name = r.get('name') or r.get('recipient_name')
            r_phone = r.get('phone') or r.get('recipient_phone')

            if r_name and r_phone:
                history = LeadShareHistory.objects.create(
                    lead=lead,
                    recipient_name=r_name,
                    recipient_phone=r_phone,
                    shared_by=request.user if request.user.is_authenticated else None
                )
                created_records.append(history)

        return Response({"message": f"Logged share for {len(created_records)} recipients"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='share-history')
    def get_share_history(self, request, pk=None):
        lead = self.get_object()
        history = lead.share_history.all().order_by('-shared_at')
        serializer = LeadShareHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='previous-recipients')
    def get_previous_recipients(self, request):
        recipients = LeadShareHistory.objects.values('recipient_name', 'recipient_phone').distinct()
        return Response(recipients)


# --- 2. Newsletter Subscriber ViewSet ---
class NewsletterSubscriberViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    serializer_class = NewsletterSubscriberSerializer

    # --- Send Bulk Email ---
    @action(detail=False, methods=['post'], url_path='send-email')
    def send_email(self, request):
        recipients = request.data.get('recipients', []) 
        subject = request.data.get('subject')
        body = request.data.get('body')

        if not recipients or not subject or not body:
            return Response({"error": "Recipients, subject, and body are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            messages = []
            from_email = settings.DEFAULT_FROM_EMAIL or 'noreply@xpertai.com'
            
            for email in recipients:
                messages.append((subject, body, from_email, [email]))

            sent_count = send_mass_mail(tuple(messages), fail_silently=False)

            return Response({"message": f"Successfully sent {sent_count} emails."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Email Error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- 3. Email Template ViewSet ---
class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all().order_by('-updated_at')
    serializer_class = EmailTemplateSerializer


# --- 4. CHATBOT FLOW HANDLER ---
@api_view(['POST'])
def chat_flow_handler(request):
    try:
        current_field = request.data.get('current_field') 
        answer = request.data.get('answer')
        flow_data = request.session.get('chatbot_flow_data', {})
        
        if current_field:
            current_step_obj = ChatbotFlowStep.objects.filter(field_to_save=current_field).first()
            if current_step_obj and current_step_obj.is_required and not answer:
                return Response({
                    "next_question": current_step_obj.question_text, 
                    "next_field": current_field, 
                    "is_complete": False, 
                    "error": "This field is required."
                })

        if current_field:
            flow_data[current_field] = answer if answer else ""
            request.session['chatbot_flow_data'] = flow_data 
            request.session.modified = True 
            
        last_order = 0
        if current_field:
            last_step = ChatbotFlowStep.objects.filter(field_to_save=current_field).first()
            if last_step: last_order = last_step.step_order
        
        next_step = ChatbotFlowStep.objects.filter(step_order__gt=last_order).order_by('step_order').first()

        if next_step:
            return Response({
                "next_question": next_step.question_text,
                "next_field": next_step.field_to_save,
                "is_complete": False
            })
        else:
            Lead.objects.create(
                name=flow_data.get('name', 'Unknown'),
                email=flow_data.get('email', ''),
                phone=flow_data.get('phone', ''),
                service=flow_data.get('service', 'General'),
                message=flow_data.get('message', ''),
                company=flow_data.get('company', ''),
                source="chatbot"
            )
            
            if 'chatbot_flow_data' in request.session:
                del request.session['chatbot_flow_data']
            
            return Response({
                "next_question": "Thank you! We will contact you shortly.",
                "is_complete": True,
                "action": "lead_captured"
            })
        
    except Exception as e:
        print(f"Error: {e}")
        first_step = ChatbotFlowStep.objects.order_by('step_order').first()
        return Response({
            "error": "Error occurred. Restarting.",
            "next_question": first_step.question_text if first_step else "Hi",
            "next_field": first_step.field_to_save if first_step else "name",
            "is_complete": False
        })