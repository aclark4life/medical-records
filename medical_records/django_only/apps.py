from django.apps import AppConfig


class MedicalRecordsDjangoConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "medical_records.django_only"
    label = "medical_records"
