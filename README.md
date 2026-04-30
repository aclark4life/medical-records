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

Both sub-apps are standard Django apps. Add one (or both) to your project's `INSTALLED_APPS` and run commands with your project's settings module.

**`medical_records.wagtail` — Wagtail CMS app**

Run migrations, set up the page tree, and seed sample data:

```bash
django-admin migrate
django-admin createsuperuser
django-admin setup_wagtail
django-admin create_patient_pages 20
django-admin runserver
```

**`medical_records.django` — Plain Django app**

Seed patient records directly into MongoDB:

```bash
django-admin create_patients 20
django-admin create_patients 20 --flush
django-admin create_patients 20 --mongodb-uri mongodb://localhost:27017/mydb
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

| Command | App | Description |
|---|---|---|
| `setup_wagtail [--force]` | `medical_records.wagtail` | Create root → home → patient index page hierarchy |
| `create_patient_pages <n> [--flush]` | `medical_records.wagtail` | Generate `n` sample patient pages |
| `create_patients <n> [--flush] [--mongodb-uri URI]` | `medical_records.django` | Generate `n` patient records |
