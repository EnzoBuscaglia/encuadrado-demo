from django.contrib import admin

from marketplace.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")
    ordering = ("name",)
    readonly_fields = ("name", "email")
