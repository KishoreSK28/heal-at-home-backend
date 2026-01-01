from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        if os.getenv("AUTO_SETUP") == "True":
            try:
                from django.core.management import call_command
                call_command("init_admin")
            except Exception:
                pass
