from django.core.exceptions import ValidationError
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    duration = models.DurationField()
    price = models.PositiveIntegerField(help_text="CLP price in pesos (e.g. 35700 = $35.700)")
    capacity = models.PositiveIntegerField(null=True, blank=True)
    is_online = models.BooleanField()
    location = models.CharField(max_length=255, blank=True)
    video_call_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.is_online and not self.video_call_url:
            raise ValidationError("Online events must have a video_call_url.")
        if not self.is_online and not self.location:
            raise ValidationError("In-person events must have a location.")


class DigitalContent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    file_url = models.URLField()

    def __str__(self):
        return self.name


class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
