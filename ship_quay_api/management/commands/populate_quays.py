from django.core.management.base import BaseCommand
from ship_quay_api.models import Quay

class Command(BaseCommand):
    help = "Populate the database with initial quays"

    def handle(self, *args, **kwargs):
        Quay.objects.create(
            name="Quay 1",
            quay_type="General",
            capacity=5,
            length_m=200,
            draft_m=10,
            tools=["cargo handling"]
        )
        Quay.objects.create(
            name="Quay 2",
            quay_type="Passenger",
            capacity=3,
            length_m=150,
            draft_m=8,
            tools=["passenger transport", "cargo handling"]
        )
        self.stdout.write(self.style.SUCCESS("Database populated with initial quays."))
