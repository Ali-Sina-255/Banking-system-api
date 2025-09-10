from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedModel

User = get_user_model()


class Profile(TimeStampedModel):
    class Salutation(models.TextChoices):
        MR = "mr", _("Mr")
        MRS = "mrs", _("Mrs")
        MISS = "miss", _("Miss")

    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")

    class MaritalStatus(models.TextChoices):
        MARRIED = "married", _("Married")
        SINGLE = "single", _("Single")
        DIVORCED = "divorced", _("Divorced")
        WIDOWED = "widowed", _("Widowed")
        SEPARATE = "separated", _("Separated")
        UNKNOWN = "unknown", _("Unknown")

    class IdentificationMeans(models.TextChoices):
        DRIVER_LICENSE = "driver_license", _("Driver License")
        NATIONAL_ID = "national_id", _("National ID")
        PASSPORT = "passport", _("Passport")

    class EmploymentStatus(models.TextChoices):
        SELF_EMPLOYED = "self_employed", _("Self Employed")
        EMPLOYED = "employed", _("Employed")
        UNEMPLOYED = "unemployed", _("Unemployed")
        RETIRED = "retired", _("Retired")
        STUDENT = "student", _("Student")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profiles")

    title = models.CharField(
        verbose_name=_("Salutation"),
        max_length=5,
        choices=Salutation.choices,
        default=Salutation.MR,
    )

    gender = models.CharField(
        _("Gender"),
        max_length=50,
        choices=Gender.choices,
        default=Gender.MALE,
    )

    date_of_birth = models.DateField(
        _("Date of Birth"), default=settings.DEFAULT_BIRTHDAY
    )

    country_of_birth = models.CharField(
        _("Country of Birth"), default=settings.DEFAULT_COUNTRY
    )

    place_of_birth = models.CharField(
        _("Place of Birth"), default=settings.DEFAULT_COUNTRY
    )

    marital_status = models.CharField(
        _("Marital Status"),
        max_length=50,
        choices=MaritalStatus.choices,
        default=MaritalStatus.UNKNOWN,
    )

    means_of_identification = models.CharField(
        _("Means of Identification"),
        max_length=50,
        choices=IdentificationMeans.choices,
        default=IdentificationMeans.DRIVER_LICENSE,
    )

    id_issue_date = models.DateField(
        _("ID or Passport Issue Date"), default=settings.DEFAULT_DATE
    )

    id_expiry_date = models.DateField(
        _("ID or Passport Expiry Date"), default=settings.DEFAULT_EXPIRY_DATE
    )

    passport_number = models.CharField(
        _("Passport Number"), max_length=40, blank=True, null=True
    )

    nationality = models.CharField(_("Nationality"), max_length=30, default="Unknown")

    phone_number = PhoneNumberField(
        _("Phone Number"), max_length=30, default=settings.DEFAULT_PHONE_NUMBER
    )

    address = models.CharField(_("Address"), max_length=100)
