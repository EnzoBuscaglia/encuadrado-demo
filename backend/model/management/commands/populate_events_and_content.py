import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from model.models import DigitalContent, DiscountCode, Event


class Command(BaseCommand):
    help = "Seeds the database with dummy events, content, and discount codes"

    def handle(self, *args, **options):
        # Clear previous data
        Event.objects.all().delete()
        DigitalContent.objects.all().delete()
        DiscountCode.objects.all().delete()

        base_date = now()

        # Create 15 events
        for i in range(15):
            is_online = i % 2 == 0
            base_price = 10000 + (i * 1700)
            price = base_price + random.randint(0, 9)
            Event.objects.create(
                name=f"Evento {i+1}",
                description=f"Descripción detallada del evento {i+1}. Aprende sobre cosas útiles.",
                start_time=base_date + timedelta(days=i + 1),
                duration=timedelta(hours=(1 + i % 3)),
                price=price,
                capacity=(None if i % 5 == 0 else 50 + i * 2),
                is_online=is_online,
                video_call_url=f"https://meet.example.com/evento{i+1}" if is_online else "",
                location=f"Av. Siempreviva {100 + i}" if not is_online else "",
            )

        # Create 15 digital contents
        for i in range(15):
            base_price = 5000 + (i * 1200)
            price = base_price + random.randint(0, 9)
            DigitalContent.objects.create(
                name=f"Contenido Digital {i+1}",
                description=f"Contenido descargable número {i+1}. Ebook, guía o curso en PDF.",
                price=price,
                file_url=f"https://downloads.example.com/content_{i+1}.pdf",
            )

        # Create 5 discount codes
        DiscountCode.objects.bulk_create(
            [
                DiscountCode(code="WELCOME10", discount_percentage=10, is_active=True),
                DiscountCode(code="SUMMER15", discount_percentage=15, is_active=True),
                DiscountCode(code="FLASH25", discount_percentage=25, is_active=True),
                DiscountCode(code="DEMO50", discount_percentage=50, is_active=False),  # inactive
                DiscountCode(code="FREE100", discount_percentage=100, is_active=True),
            ]
        )

        self.stdout.write(
            self.style.SUCCESS("✔ Dummy data loaded: 15 events, 15 contents, 5 codes.")
        )
