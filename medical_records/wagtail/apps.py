from django.apps import AppConfig


class MedicalWagtailConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "medical_records.wagtail"
    label = "medical_records_wagtail"
    verbose_name = "Medical Records (Wagtail)"
