from django.contrib import admin

from model.models import DigitalContent, DiscountCode, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_time", "duration", "price", "is_online", "capacity")
    list_filter = ("is_online", "start_time")
    search_fields = ("name", "description")
    ordering = ("-start_time",)
    readonly_fields = ()  # You can add e.g. created_at here later


@admin.register(DigitalContent)
class DigitalContentAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "file_url")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percentage", "is_active")
    search_fields = ("code",)
    list_filter = ("is_active",)
