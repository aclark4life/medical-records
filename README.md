# Medical Records

A sample patient record management application built with [Wagtail CMS](https://wagtail.org/) and [MongoDB](https://www.mongodb.com/), using [`django-mongodb-backend`](https://github.com/mongodb-labs/django-mongodb-backend) for document storage and field-level encryption of sensitive data (SSN, billing info).

## Project structure

```
medical_records/
├── django/          # Core data models (Patient, PatientRecord, Billing)
└── wagtail/         # Wagtail CMS integration (pages, admin, settings)
```

The two sub-apps can be used independently. `medical_records.wagtail` provides the full CMS-driven frontend; `medical_records.django` exposes the same models through the standard Django admin.

## Requirements

- Python 3.11+
- MongoDB (local or Atlas)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Configuration

Set the following environment variables before running the app:

| Variable | Default | Description |
|---|---|---|
| `MONGODB_URI` | `mongodb://localhost:27017/medical_records` | MongoDB connection URI |
| `DJANGO_SECRET_KEY` | `dev-secret-key-change-in-production` | Django secret key |
| `DEBUG` | `true` | Enable debug mode |
| `ALLOWED_HOSTS` | `localhost 127.0.0.1` | Space-separated list of allowed hosts |

## Usage

All commands use `DJANGO_SETTINGS_MODULE=medical_records.wagtail.settings.base`.

**Run migrations:**
```bash
django-admin migrate --settings=medical_records.wagtail.settings.base
```

**Create a superuser:**
```bash
django-admin createsuperuser --settings=medical_records.wagtail.settings.base
```

**Set up the Wagtail page tree** (run once after migrate):
```bash
django-admin setup_wagtail --settings=medical_records.wagtail.settings.base
```

**Generate sample patient pages:**
```bash
django-admin create_patient_pages 20 --settings=medical_records.wagtail.settings.base
```

**Start the development server:**
```bash
django-admin runserver --settings=medical_records.wagtail.settings.base
```

## URLs

| URL | Description |
|---|---|
| `http://localhost:8000/` | Public site |
| `http://localhost:8000/cms/` | Wagtail admin |
| `http://localhost:8000/admin/` | Django admin |

## Data model

Sensitive fields (`ssn`, `cc_number`) are stored using `EncryptedCharField` and `EncryptedEmbeddedModelField` from `django-mongodb-backend`. The `PatientRecord` and `Billing` types are embedded documents (no separate collections).

```
PatientPage (Wagtail page)
└── patient_record: PatientRecord (embedded)
    └── billing: Billing (embedded, encrypted)
```

## Management commands

| Command | Description |
|---|---|
| `setup_wagtail [--force]` | Create root → home → patient index page hierarchy |
| `create_patient_pages <n> [--flush]` | Generate `n` sample patient pages |
| `create_patient <n> [--flush] [--mongodb-uri URI]` | Generate `n` records in the base Django app |
