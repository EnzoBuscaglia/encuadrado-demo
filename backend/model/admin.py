import re
from datetime import timedelta

from django import forms
from django.contrib import admin

from model.models import DigitalContent, DiscountCode, Event


class EventAdminForm(forms.ModelForm):
    duration = forms.CharField(
        help_text="Format: HH:MM (for instance, use 01:30 for one and a half hour)",
        label="Duration (HH:MM)",
    )

    class Meta:
        model = Event
        fields = "__all__"

    def clean_duration(self):
        match = re.fullmatch(r"(\d{1,2}):([0-5]\d)", self.cleaned_data["duration"].strip())
        if not match:
            raise forms.ValidationError("Use the exact format HH:MM (e.g. 01:30 or 2:00)")
        return timedelta(hours=int(match[1]), minutes=int(match[2]))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        duration = getattr(self.instance, "duration", None)
        if duration:
            minutes = duration.total_seconds() // 60
            self.fields["duration"].widget.format_value = (
                lambda _: f"{int(minutes // 60):02d}:{int(minutes % 60):02d}"
            )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = (
        "name",
        "start_time",
        "get_duration_display",
        "get_price_display",
        "is_online",
        "capacity",
    )
    list_filter = ("is_online", "start_time")
    search_fields = ("name", "description")
    ordering = ("-start_time",)
    readonly_fields = ()

    @admin.display(description="Duration")
    def get_duration_display(self, obj):
        total_minutes = int(obj.duration.total_seconds() // 60)
        hours, minutes = divmod(total_minutes, 60)
        return f"{hours}h {minutes}m" if hours else f"{minutes}m"

    @admin.display(description="Price")
    def get_price_display(self, obj):
        return f"${obj.price:,}".replace(",", ".")


@admin.register(DigitalContent)
class DigitalContentAdmin(admin.ModelAdmin):
    list_display = ("name", "get_price_display", "file_url")
    search_fields = ("name", "description")
    ordering = ("name",)

    @admin.display(description="Price")
    def get_price_display(self, obj):
        return f"${obj.price:,}".replace(",", ".")


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percentage", "is_active")
    search_fields = ("code",)
    list_filter = ("is_active",)
