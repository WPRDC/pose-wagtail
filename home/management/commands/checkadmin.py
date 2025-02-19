from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Check if at least one (1) superuser was previously created and skip creation of a new one, if so."

    def handle(self, *args, **options):
        try:
            if User.objects.filter(is_superuser=True).count() > 0:
                exit(0)
            exit(1)
        except Exception:
            exit(1)
