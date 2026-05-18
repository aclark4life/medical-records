import os
import random

from django.core.management.base import BaseCommand

from faker import Faker

from medical_records.models import Patient, PatientRecord, Billing


class Command(BaseCommand):
    help = "Create patients with embedded patient records and billing using Faker. Optionally set MONGODB_URI."

    def add_arguments(self, parser):
        parser.add_argument(
            "num_patients", type=int, help="Number of patients to create"
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing patients before creating new ones",
        )
        parser.add_argument(
            "--mongodb-uri",
            type=str,
            help="MongoDB connection URI to set as MONGODB_URI env var",
        )
        parser.add_argument(
            "--skip-collection-check",
            action="store_true",
            help="Skip checking if the encrypted collection exists before creating patients",
        )

    def _encrypted_collections_exist(self):
        """Return True if the encrypted database has been migrated."""
        try:
            from django.db import connections

            conn = connections["encrypted"]
            conn.ensure_connection()
            collection_names = conn.database.list_collection_names()
            return "medical_records_patient" in collection_names
        except Exception:
            return False

    def handle(self, *args, **options):
        fake = Faker()

        num_patients = options["num_patients"]

        # Set MONGODB_URI if provided
        if options.get("mongodb_uri"):
            os.environ["MONGODB_URI"] = options["mongodb_uri"]
            self.stdout.write(
                self.style.SUCCESS(f"MONGODB_URI set to: {options['mongodb_uri']}")
            )

        if not options["skip_collection_check"] and not self._encrypted_collections_exist():
            self.stderr.write(
                self.style.ERROR(
                    "Encrypted collections do not exist. "
                    "Run 'manage.py migrate --database encrypted' first."
                )
            )
            return

        # Optionally flush
        if options["flush"]:
            Patient.objects.all().delete()
            self.stdout.write(self.style.WARNING("Deleted all existing patients."))

        for _ in range(num_patients):
            billing = Billing(
                cc_type=fake.credit_card_provider(), cc_number=fake.credit_card_number()
            )
            record = PatientRecord(
                ssn=fake.ssn(),
                billing=billing,
                bill_amount=round(random.uniform(50.0, 5000.0), 2),
            )
            patient = Patient(
                patient_name=fake.name(),
                patient_id=random.randint(100000, 999999),
                patient_record=record,
            )
            patient.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created Patient: {patient.patient_name} ({patient.patient_id})"
                )
            )
            self.stdout.write(f"  SSN: {record.ssn}")
            self.stdout.write(f"  Billing CC Type: {billing.cc_type}")
            self.stdout.write(f"  Billing CC Number: {billing.cc_number}")
            self.stdout.write(f"  Bill Amount: ${record.bill_amount}")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {num_patients} patient(s).")
        )
