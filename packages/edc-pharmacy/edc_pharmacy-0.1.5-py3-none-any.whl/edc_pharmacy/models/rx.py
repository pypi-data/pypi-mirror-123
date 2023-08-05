from django.db import models
from django.db.models import PROTECT
from edc_constants.constants import NEW
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_model import models as edc_models
from edc_randomization.site_randomizers import site_randomizers
from edc_search.model_mixins import SearchSlugManager
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import formatted_age, get_utcnow

from ..choices import PRESCRIPTION_STATUS
from .medication import Medication
from .search_slug_model_mixin import SearchSlugModelMixin
from .subject import Subject


class Manager(SearchSlugManager, models.Manager):
    def get_by_natural_key(self, subject_identifier, report_datetime):
        return self.get(
            subject_identifier=subject_identifier, report_datetime=report_datetime
        )


class Rx(
    NonUniqueSubjectIdentifierFieldMixin,
    SiteModelMixin,
    SearchSlugModelMixin,
    edc_models.BaseUuidModel,
):

    registered_subject = models.ForeignKey(
        Subject,
        verbose_name="Subject Identifier",
        on_delete=PROTECT,
        null=True,
        blank=False,
    )

    report_datetime = models.DateTimeField(default=get_utcnow)

    rx_date = models.DateField(verbose_name="Date RX written", default=get_utcnow)

    status = models.CharField(max_length=25, default=NEW, choices=PRESCRIPTION_STATUS)

    medication = models.ForeignKey(Medication, on_delete=PROTECT, null=True)

    refill = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of times this prescription may be refilled",
    )

    rando_sid = models.CharField(max_length=25, null=True, blank=True)

    randomizer_name = models.CharField(max_length=25, null=True, blank=True)

    weight_in_kgs = models.DecimalField(
        max_digits=6, decimal_places=1, null=True, blank=True
    )

    clinician_initials = models.CharField(max_length=3, null=True)

    notes = models.TextField(
        max_length=250,
        null=True,
        blank=True,
        help_text="Private notes for pharmacist only",
    )

    on_site = CurrentSiteManager()

    objects = Manager()

    history = edc_models.HistoricalRecords()

    def __str__(self):
        return (
            f"{self.medication} "
            f"{self.registered_subject.subject_identifier} {self.registered_subject.initials} "
            f"{formatted_age(born=self.registered_subject.dob, reference_dt=get_utcnow())} "
            f"{self.registered_subject.gender}"
        )

    def natural_key(self):
        return (
            self.subject_identifier,
            self.report_datetime,
        )

    def save(self, *args, **kwargs):
        self.subject_identifier = self.registered_subject.subject_identifier
        if self.randomizer_name:
            randomizer = site_randomizers.get(self.randomizer_name)
            self.rando_sid = (
                randomizer.model_cls()
                .objects.get(subject_identifier=self.subject_identifier)
                .sid
            )
        super().save(*args, **kwargs)

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"
