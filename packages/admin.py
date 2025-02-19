from django.contrib import admin

from .models import TourPackage


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = [
        "product_code",
        "title",
        "category",
        "airline",
        "duration",
        "price",
    ]
    search_fields = ["product_code", "title", "category"]
    list_filter = ["category", "airline", "duration"]
