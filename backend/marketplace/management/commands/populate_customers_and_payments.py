import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from marketplace.models import ContentDownload, Customer, DiscountCode, EventRegistration
from model.models import DigitalContent, Event


class Command(BaseCommand):
    help = "Seeds Customers + EventRegistrations + ContentDownloads"

    def handle(self, *args, **kwargs):
        # Clear previous data
        EventRegistration.objects.all().delete()
        ContentDownload.objects.all().delete()
        Customer.objects.all().delete()

        # Create 10 customers
        customers = []
        for i in range(10):
            customer = Customer.objects.create(
                name=f"Cliente {i+1}",
                email=f"cliente{i+1}@demo.com",
                password="dummy-pass",  # Not used in frontend
            )
            customers.append(customer)

        events = list(Event.objects.all())
        contents = list(DigitalContent.objects.all())
        discounts = list(DiscountCode.objects.filter(is_active=True))

        now_ts = now()

        # Register each customer in 1–3 events
        for customer in customers:
            selected_events = random.sample(events, k=min(len(events), random.randint(1, 3)))
            for event in selected_events:
                base_price = event.price
                discount = random.choice(discounts + [None])
                discount_amount = (
                    (discount.discount_percentage * base_price // 100) if discount else 0
                )
                final_price = base_price - discount_amount
                paid = final_price % 10 < 8  # Simulate paid based on spec
                paid_at = now_ts - timedelta(days=random.randint(0, 10)) if paid else None

                EventRegistration.objects.create(
                    customer=customer,
                    event=event,
                    normal_price=base_price,
                    final_price=final_price,
                    discount_code=discount,
                    payment_status="paid" if paid else "failed",
                    paid_at=paid_at,
                )

        # Simulate digital content downloads for each customer
        for customer in customers:
            selected_contents = random.sample(
                contents, k=min(len(contents), random.randint(0, 2))
            )
            for content in selected_contents:
                base_price = content.price
                discount = random.choice(discounts + [None])
                discount_amount = (
                    (discount.discount_percentage * base_price // 100) if discount else 0
                )
                final_price = base_price - discount_amount
                paid = base_price % 10 < 8
                paid_at = now_ts - timedelta(days=random.randint(0, 10)) if paid else None

                ContentDownload.objects.create(
                    customer=customer,
                    content=content,
                    normal_price=base_price,
                    final_price=final_price,
                    discount_code=discount,
                    payment_status="paid" if paid else "failed",
                    paid_at=paid_at,
                )

        self.stdout.write(
            self.style.SUCCESS("✔ Dummy customers, registrations, and downloads loaded.")
        )
