from django.db import models
from django_mongodb_backend.fields import (
    EmbeddedModelField,
    EncryptedCharField,
    EncryptedEmbeddedModelField,
)
from django_mongodb_backend.models import EmbeddedModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import CharBlock, RichTextBlock, StructBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index


class Billing(EmbeddedModel):
    cc_type = models.CharField(max_length=50)
    cc_number = models.CharField(max_length=20)


class PatientRecord(EmbeddedModel):
    ssn = EncryptedCharField(max_length=11)
    billing = EncryptedEmbeddedModelField(Billing)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)


class HomePage(Page):
    template = "medical_records/wagtail/home/home_page.html"

    intro = RichTextField(blank=True)
    body = StreamField(
        [
            (
                "stat_block",
                StructBlock(
                    [
                        ("label", CharBlock()),
                        ("value", CharBlock()),
                        ("icon", CharBlock(required=False)),
                    ],
                    icon="pick",
                ),
            ),
            ("rich_text", RichTextBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    subpage_types = ["medical_records_wagtail.PatientIndexPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["total_patients"] = PatientPage.objects.live().count()
        context["total_records"] = PatientPage.objects.live().filter(
            patient_record__isnull=False
        ).count()
        return context

    class Meta:
        verbose_name = "Home Page"


class PatientIndexPage(Page):
    template = "medical_records/wagtail/patients/patient_index_page.html"

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["medical_records_wagtail.HomePage"]
    subpage_types = ["medical_records_wagtail.PatientPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["patients"] = (
            PatientPage.objects.child_of(self).live().order_by("patient_name")
        )
        return context

    class Meta:
        verbose_name = "Patient Index Page"


class PatientPage(Page):
    template = "medical_records/wagtail/patients/patient_page.html"

    patient_name = models.CharField(max_length=255)
    patient_id = models.BigIntegerField()
    patient_record = EmbeddedModelField(PatientRecord, null=True, blank=True)
    notes = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("patient_name"),
        index.FilterField("patient_id"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("patient_name"),
                FieldPanel("patient_id"),
            ],
            heading="Patient Info",
        ),
        FieldPanel("notes"),
    ]

    parent_page_types = ["medical_records_wagtail.PatientIndexPage"]
    subpage_types = []

    def __str__(self):
        return f"{self.patient_name} ({self.patient_id})"

    class Meta:
        verbose_name = "Patient Page"
        verbose_name_plural = "Patient Pages"
