from django.core.management.base import BaseCommand
from ../../../models import HomePage


class Command(BaseCommand):
    help = "Set up database to serve data."

    def handle(self, *args, **options):
        try:
            if HomePage.objects.filter(is_superuser=True).count() > 0:
                exit(0)
            exit(1)
        except Exception:
            exit(1)
