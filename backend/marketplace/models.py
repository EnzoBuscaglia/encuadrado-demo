from django.db import models

from model.models import DigitalContent, DiscountCode, Event


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} ({self.email})"


class PaymentStatus(models.TextChoices):
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"


class EventRegistration(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="event_registrations"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    created_at = models.DateTimeField(auto_now_add=True)
    normal_price = models.PositiveIntegerField()
    final_price = models.PositiveIntegerField()
    discount_code = models.ForeignKey(
        DiscountCode, null=True, blank=True, on_delete=models.SET_NULL
    )
    payment_status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.FAILED,
    )
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer.name} -> {self.event.name}"


class ContentDownload(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="content_downloads"
    )
    content = models.ForeignKey(
        DigitalContent, on_delete=models.CASCADE, related_name="downloads"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    normal_price = models.PositiveIntegerField()
    final_price = models.PositiveIntegerField()
    discount_code = models.ForeignKey(
        DiscountCode, null=True, blank=True, on_delete=models.SET_NULL
    )
    payment_status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.FAILED,
    )
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer.name} -> {self.content.name}"
