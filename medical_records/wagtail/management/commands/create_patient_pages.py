import random
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from wagtail.models import Locale, Page

from medical_records.wagtail.models import (
    Billing,
    PatientIndexPage,
    PatientPage,
    PatientRecord,
)


class Command(BaseCommand):
    help = "Create sample PatientPage entries under the PatientIndexPage."

    def add_arguments(self, parser):
        parser.add_argument("num_patients", type=int, help="Number of patient pages to create")
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing patient pages before creating new ones",
        )

    def handle(self, *args, **options):
        fake = Faker()

        try:
            index = PatientIndexPage.objects.live().first()
        except PatientIndexPage.DoesNotExist:
            raise CommandError(
                "No PatientIndexPage found. Run `manage.py setup_wagtail` first."
            )

        if not index:
            raise CommandError(
                "No PatientIndexPage found. Run `manage.py setup_wagtail` first."
            )

        if options["flush"]:
            deleted, _ = PatientPage.objects.child_of(index).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing patient page(s)."))

        ct, _ = ContentType.objects.get_or_create(
            app_label="medical_records_wagtail", model="patientpage"
        )
        locale = Locale.objects.get(language_code="en")

        for _ in range(options["num_patients"]):
            name = fake.name()
            patient_id = random.randint(100000, 999999)
            slug = f"patient-{patient_id}"

            billing = Billing(
                cc_type=fake.credit_card_provider(),
                cc_number=fake.credit_card_number(),
            )
            record = PatientRecord(
                ssn=fake.ssn(),
                billing=billing,
                bill_amount=round(random.uniform(50.0, 5000.0), 2),
            )

            page = PatientPage(
                title=name,
                patient_name=name,
                patient_id=patient_id,
                patient_record=record,
                slug=slug,
                content_type=ct,
                locale=locale,
            )
            index.add_child(instance=page)

            self.stdout.write(
                self.style.SUCCESS(f"Created patient page: {name} ({patient_id})")
            )

        self.stdout.write(
            self.style.SUCCESS(f"Done. Created {options['num_patients']} patient page(s).")
        )
