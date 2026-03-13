from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a default superuser (admin/admin)'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@xpertai.com',
                password='XpeertLand@123'  # Change this to a strong password
            )
            self.stdout.write(self.style.SUCCESS('✅ Superuser "XpertAdmin" created! Password: XpeertLand@123'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Superuser "admin" already exists.'))