from django.contrib import admin

from marketplace.models import ContentDownload, Customer, EventRegistration


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")
    ordering = ("name",)
    readonly_fields = ("name", "email")


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "customer__name",
        "customer__email",
        "payment_status",
        "paid_at",
        "final_price",
        "created_at",
    )
    search_fields = ("customer__name", "customer__email", "event__name")
    list_filter = ("payment_status", "event__start_time")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "paid_at")


@admin.register(ContentDownload)
class ContentDownloadAdmin(admin.ModelAdmin):
    list_display = (
        "content",
        "customer__name",
        "customer__email",
        "payment_status",
        "paid_at",
        "final_price",
        "created_at",
    )
    search_fields = ("customer__name", "customer__email", "content__name")
    list_filter = ("payment_status",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "paid_at")
