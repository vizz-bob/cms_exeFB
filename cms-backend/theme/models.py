from django.db import models

# --- THEME SETTING DISABLED ---
# class ThemeSetting(models.Model):
#     name = models.CharField(max_length=100, default="Default Theme")
#     is_active = models.BooleanField(default=True)
#     ... (disabled)

# --- CHATBOT FLOW STEP (ACTIVE) ---
class ChatbotFlowStep(models.Model):
    FIELD_CHOICES = [
        ('name', 'Applicant Name'),
        ('email', 'Email Address'),
        ('phone', 'Phone Number'),
        ('service', 'Service Interest'),
        ('message', 'Message/Final Query'),
    ]

    question_text = models.CharField(max_length=255, help_text="The question the bot asks.")
    field_to_save = models.CharField(max_length=50, choices=FIELD_CHOICES, unique=True, 
                                     help_text="The Lead field this question's answer should populate.")
    step_order = models.PositiveIntegerField(default=0, help_text="Order in which questions are asked.")
    is_required = models.BooleanField(default=True)

    class Meta:
        ordering = ['step_order']
        verbose_name = "Chatbot Flow Step"
        verbose_name_plural = "Chatbot Flow Steps"

    def __str__(self):
        return f"Step {self.step_order}: {self.question_text}"