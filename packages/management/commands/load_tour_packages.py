import csv

from django.core.management.base import BaseCommand

from packages.models import TourPackage


class Command(BaseCommand):
    help = "Load tour packages from CSV file"

    def handle(self, *args, **kwargs):
        # Clear existing data
        TourPackage.objects.all().delete()

        # Read CSV and insert data
        with open("data/tour_packages.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                TourPackage.objects.create(
                    product_code=row["product_code"],
                    category=row["category"],
                    title=row["title"],
                    description=row["description"],
                    airline=row["airline"],
                    airline_logo=row["airline_logo"],
                    departure_days=row["departure_days"],
                    duration=row["duration"],
                    price=row["price"],
                    master_code=row["master_code"],
                    product_no=row["product_no"],
                    list_url=row["list_url"],
                )

        self.stdout.write(self.style.SUCCESS("Successfully loaded tour packages data"))
