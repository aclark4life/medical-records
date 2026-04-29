from django.apps import AppConfig


class MedicalRecordsDjangoConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "medical_records.django"
    label = "medical_records"
