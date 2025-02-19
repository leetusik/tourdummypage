from django.db import models

# Create your models here.


class TourPackage(models.Model):
    # Core fields
    product_code = models.CharField(max_length=10, primary_key=True)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Airline info
    airline = models.CharField(max_length=50)
    airline_logo = models.CharField(max_length=100)

    # Schedule and duration
    departure_days = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)

    # Price and product details
    price = models.CharField(max_length=20)  # Stored as string to preserve formatting
    master_code = models.CharField(max_length=10)
    product_no = models.CharField(max_length=20)
    list_url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.product_code} - {self.title}"

    class Meta:
        db_table = "tour_packages"
        verbose_name = "Tour Package"
        verbose_name_plural = "Tour Packages"
