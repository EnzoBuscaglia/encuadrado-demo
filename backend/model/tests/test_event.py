from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now

from model.models import Event


class EventValidationTest(TestCase):
    def test_online_event_requires_video_call_url(self):
        event = Event(
            name="Test Online",
            description="Testing online event without URL",
            start_time=now(),
            duration=timedelta(hours=1),
            price=10000,
            capacity=50,
            is_online=True,
            video_call_url="",  # <- Missing
            location="Optional location",
        )
        with self.assertRaises(ValidationError) as context:
            event.full_clean()
        self.assertIn("video_call_url", str(context.exception))

    def test_inperson_event_requires_location(self):
        event = Event(
            name="Test Offline",
            description="Testing in-person event without location",
            start_time=now(),
            duration=timedelta(hours=1),
            price=10000,
            capacity=50,
            is_online=False,
            video_call_url="https://zoom.us/xyz",  # Irrelevant
            location="",  # <- Missing
        )
        with self.assertRaises(ValidationError) as context:
            event.full_clean()
        self.assertIn("location", str(context.exception))

    def test_valid_online_event_passes_clean(self):
        event = Event(
            name="Valid Online",
            description="This should pass validation",
            start_time=now(),
            duration=timedelta(hours=2),
            price=25000,
            capacity=100,
            is_online=True,
            video_call_url="https://meet.google.com/abc",
            location="Irrelevant",
        )
        try:
            event.full_clean()  # Should not raise
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_valid_inperson_event_passes_clean(self):
        event = Event(
            name="Valid In-person",
            description="This should also pass validation",
            start_time=now(),
            duration=timedelta(hours=2),
            price=25000,
            capacity=100,
            is_online=False,
            video_call_url="",  # Irrelevant
            location="Av. Apoquindo 1234, Santiago",
        )
        try:
            event.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")
