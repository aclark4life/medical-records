import django.db.models.deletion
import django_mongodb_backend.fields
import medical_records.wagtail.models
import wagtail.blocks
import wagtail.fields
import wagtail.search.index
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.CreateModel(
            name="Billing",
            fields=[
                (
                    "id",
                    django_mongodb_backend.fields.ObjectIdAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("cc_type", models.CharField(max_length=50)),
                ("cc_number", models.CharField(max_length=20)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="PatientRecord",
            fields=[
                (
                    "id",
                    django_mongodb_backend.fields.ObjectIdAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("ssn", django_mongodb_backend.fields.EncryptedCharField(max_length=11)),
                (
                    "billing",
                    django_mongodb_backend.fields.EncryptedEmbeddedModelField(
                        embedded_model=medical_records.wagtail.models.Billing
                    ),
                ),
                ("bill_amount", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("intro", wagtail.fields.RichTextField(blank=True)),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "stat_block",
                                wagtail.blocks.StructBlock(
                                    [
                                        ("label", wagtail.blocks.CharBlock()),
                                        ("value", wagtail.blocks.CharBlock()),
                                        ("icon", wagtail.blocks.CharBlock(required=False)),
                                    ]
                                ),
                            ),
                            ("rich_text", wagtail.blocks.RichTextBlock()),
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
            ],
            options={"verbose_name": "Home Page"},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="PatientIndexPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("intro", wagtail.fields.RichTextField(blank=True)),
            ],
            options={"verbose_name": "Patient Index Page"},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="PatientPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("patient_name", models.CharField(max_length=255)),
                ("patient_id", models.BigIntegerField()),
                (
                    "patient_record",
                    django_mongodb_backend.fields.EmbeddedModelField(
                        blank=True,
                        embedded_model=medical_records.wagtail.models.PatientRecord,
                        null=True,
                    ),
                ),
                ("notes", wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                "verbose_name": "Patient Page",
                "verbose_name_plural": "Patient Pages",
            },
            bases=("wagtailcore.page",),
        ),
    ]
