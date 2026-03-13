from django.core.management.base import BaseCommand
from theme.models import ChatbotFlowStep

class Command(BaseCommand):
    help = 'Seeds the initial questions for the Chatbot flow'

    def handle(self, *args, **kwargs):
        self.stdout.write('🤖 Seeding Chatbot Flow...')

        # Clear existing to avoid duplicates during dev
        ChatbotFlowStep.objects.all().delete()

        questions = [
            {
                "step_order": 1,
                "question_text": "Hi there! Welcome to XpertAI. May I know your full name?",
                "field_to_save": "name",
                "is_required": True
            },
            {
                "step_order": 2,
                "question_text": "Great! Could you please share your email address so we can connect?",
                "field_to_save": "email",
                "is_required": True
            },
            {
                "step_order": 3,
                "question_text": "Thanks. A phone number would also be helpful for quick communication.",
                "field_to_save": "phone",
                "is_required": False
            },
            {
                "step_order": 4,
                "question_text": "Which service are you interested in? (e.g., Audit, CFO, Tax, Tech)",
                "field_to_save": "service",
                "is_required": True
            },
            {
                "step_order": 5,
                "question_text": "Any specific requirements or message you'd like to add?",
                "field_to_save": "message",
                "is_required": False
            }
        ]

        for q in questions:
            ChatbotFlowStep.objects.create(**q)
            self.stdout.write(f"   ✅ Added Question: {q['field_to_save']}")

        self.stdout.write(self.style.SUCCESS('🎉 Chatbot Flow Seeded!'))