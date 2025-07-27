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
        "get_customer_name",
        "get_customer_email",
        "get_normal_price",
        "get_discount_code",
        "payment_status",
        "paid_at",
        "get_final_price",
        "created_at",
    )
    search_fields = ("customer__name", "customer__email", "event__name")
    list_filter = ("payment_status", "event__start_time")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "paid_at")

    @admin.display(description="Customer Name")
    def get_customer_name(self, obj):
        return obj.customer.name

    @admin.display(description="Customer Email")
    def get_customer_email(self, obj):
        return obj.customer.email

    @admin.display(description="Normal Price")
    def get_normal_price(self, obj):
        return f"${obj.normal_price:,}".replace(",", ".")

    @admin.display(description="Final Price")
    def get_final_price(self, obj):
        return f"${obj.final_price:,}".replace(",", ".")

    @admin.display(description="Discount Code")
    def get_discount_code(self, obj):
        return obj.discount_code.code if obj.discount_code else "-"


@admin.register(ContentDownload)
class ContentDownloadAdmin(admin.ModelAdmin):
    list_display = (
        "content",
        "get_customer_name",
        "get_customer_email",
        "get_normal_price",
        "get_discount_code",
        "payment_status",
        "paid_at",
        "get_final_price",
        "created_at",
    )
    search_fields = ("customer__name", "customer__email", "content__name")
    list_filter = ("payment_status",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "paid_at")

    @admin.display(description="Customer Name")
    def get_customer_name(self, obj):
        return obj.customer.name

    @admin.display(description="Customer Email")
    def get_customer_email(self, obj):
        return obj.customer.email

    @admin.display(description="Normal Price")
    def get_normal_price(self, obj):
        return f"${obj.normal_price:,}".replace(",", ".")

    @admin.display(description="Final Price")
    def get_final_price(self, obj):
        return f"${obj.final_price:,}".replace(",", ".")

    @admin.display(description="Discount Code")
    def get_discount_code(self, obj):
        return obj.discount_code.code if obj.discount_code else "-"
