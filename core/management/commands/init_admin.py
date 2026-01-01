from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create superuser if not exists"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")
        email = os.getenv("ADMIN_EMAIL", "")

        if not username or not password:
            self.stdout.write("Admin env vars not set")
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password=password,
                email=email
            )
            self.stdout.write("✅ Superuser created")
        else:
            self.stdout.write("ℹ️ Superuser already exists")
