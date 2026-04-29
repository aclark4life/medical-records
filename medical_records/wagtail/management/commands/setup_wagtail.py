from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from wagtail.models import Locale, Page, Site

from medical_records.wagtail.models import HomePage, PatientIndexPage


class Command(BaseCommand):
    help = "Create Wagtail root page, home page, patient index, and default site."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Re-run setup even if root page already exists.",
        )

    def handle(self, *args, **options):
        if Page.objects.filter(depth=1).exists() and not options["force"]:
            self.stdout.write(self.style.WARNING("Wagtail pages already set up. Use --force to re-run."))
            return

        from django.conf import settings as django_settings

        lang = (getattr(django_settings, "LANGUAGE_CODE", "en") or "en").split("-")[0][:2]
        locale, _ = Locale.objects.get_or_create(language_code=lang)

        base_ct, _ = ContentType.objects.get_or_create(app_label="wagtailcore", model="page")
        if not Page.objects.filter(depth=1).exists():
            root = Page.add_root(title="Root", slug="root", content_type=base_ct, locale=locale)
            self.stdout.write(self.style.SUCCESS("Created root page."))
        else:
            root = Page.objects.get(depth=1)

        home_ct, _ = ContentType.objects.get_or_create(
            app_label="medical_records_wagtail", model="homepage"
        )
        home = HomePage(
            title="Medical Records",
            slug="home",
            content_type=home_ct,
            locale=locale,
            show_in_menus=False,
        )
        root.add_child(instance=home)
        self.stdout.write(self.style.SUCCESS("Created home page."))

        patient_ct, _ = ContentType.objects.get_or_create(
            app_label="medical_records_wagtail", model="patientindexpage"
        )
        patient_index = PatientIndexPage(
            title="Patients",
            slug="patients",
            content_type=patient_ct,
            locale=locale,
            intro="Browse and manage all patient records.",
            show_in_menus=True,
        )
        home.add_child(instance=patient_index)
        self.stdout.write(self.style.SUCCESS("Created patient index page."))

        if not Site.objects.filter(is_default_site=True).exists():
            Site.objects.create(
                hostname="localhost",
                port=8000,
                site_name="Medical Records",
                root_page=home,
                is_default_site=True,
            )
            self.stdout.write(self.style.SUCCESS("Created default site."))
        else:
            site = Site.objects.get(is_default_site=True)
            site.root_page = home
            site.save()
            self.stdout.write(self.style.SUCCESS("Updated default site root page."))

        self.stdout.write(self.style.SUCCESS("Wagtail setup complete."))
