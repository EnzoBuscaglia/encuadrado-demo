import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from marketplace.models import ContentDownload, Customer, DiscountCode, EventRegistration
from model.models import DigitalContent, Event


class Command(BaseCommand):
    help = "Seeds Customers + EventRegistrations + ContentDownloads"

    def handle(self, *args, **kwargs):
        self.clear_data()
        customers = self.create_customers()
        self.register_customers_in_events(customers)
        self.simulate_content_downloads(customers)
        self.stdout.write(
            self.style.SUCCESS("✔ Dummy customers, registrations, and downloads loaded.")
        )

    def clear_data(self):
        EventRegistration.objects.all().delete()
        ContentDownload.objects.all().delete()
        Customer.objects.all().delete()

    def create_customers(self):
        return [
            Customer.objects.create(name=f"Cliente {i+1}", email=f"cliente{i+1}@demo.com")
            for i in range(10)
        ]

    def register_customers_in_events(self, customers):
        events = list(Event.objects.all())
        discounts = list(DiscountCode.objects.filter(is_active=True))
        now_ts = now()

        for customer in customers:
            selected_events = random.sample(events, k=min(len(events), random.randint(1, 3)))
            for event in selected_events:
                base_price = event.price
                discount = random.choice(discounts + [None])
                discount_amount = (
                    (discount.discount_percentage * base_price // 100) if discount else 0
                )
                final_price = base_price - discount_amount
                paid = final_price % 10 < 8
                EventRegistration.objects.create(
                    customer=customer,
                    event=event,
                    normal_price=base_price,
                    final_price=final_price,
                    discount_code=discount,
                    payment_status="paid" if paid else "failed",
                    paid_at=now_ts - timedelta(days=random.randint(0, 10)) if paid else None,
                )

    def simulate_content_downloads(self, customers):
        contents = list(DigitalContent.objects.all())
        discounts = list(DiscountCode.objects.filter(is_active=True))
        now_ts = now()

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
                paid = final_price % 10 < 8
                ContentDownload.objects.create(
                    customer=customer,
                    content=content,
                    normal_price=base_price,
                    final_price=final_price,
                    discount_code=discount,
                    payment_status="paid" if paid else "failed",
                    paid_at=now_ts - timedelta(days=random.randint(0, 10)) if paid else None,
                )
