import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from djangoapp.models import CarMake, CarModel
class Command(BaseCommand):
    help = "Idempotently load the course car catalog"
    def handle(self, *args, **options):
        rows = json.loads((Path(settings.BASE_DIR)/"database/data/car_records.json").read_text())["cars"]
        for row in rows:
            make, _ = CarMake.objects.get_or_create(name=row["make"], defaults={"description": f'{row["make"]} vehicles'})
            CarModel.objects.get_or_create(car_make=make, name=row["model"], year=row["year"], defaults={"type": row["bodyType"]})
        self.stdout.write(self.style.SUCCESS(f"Loaded {CarMake.objects.count()} makes and {CarModel.objects.count()} models"))
