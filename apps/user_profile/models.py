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
        UNEMPLOYED = "unemployed", _("Un employed")
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
    city = models.CharField(_("City"), max_length=100)
    country = CountryField(_("Country"), default=settings.DEFAULT_COUNTRY)
    employment_status = models.CharField(
        _("Employment Status"),
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.SELF_EMPLOYED,
    )
    employ_name = models.CharField(
        _("Employer Name"), max_length=50, blank=True, null=True
    )
    annul_income = models.DecimalField(
        _("Annual Income"), max_digits=12, decimal_places=2, default=0.0
    )

    date_of_employment = models.DateField(
        _("Date of Employment"), blank=True, null=True
    )
    employer_address = models.CharField(
        _("Employer Address"), max_length=100, blank=True, null=True
    )

    employer_city = models.CharField(
        _("Employer City"), max_length=100, blank=True, null=True
    )

    employer_state = models.CharField(
        _("Employer State"), max_length=100, blank=True, null=True
    )

    photo = CloudinaryField(_("Photo"), blank=True, null=True)

    photo_url = models.URLField(_("Photo URL"), blank=True, null=True)
    id_photo = CloudinaryField(_("ID Photo"), max_length=100, blank=True, null=True)
    id_photo_url = models.URLField(_("ID Photo URL"), blank=True, null=True)

    signature_photo = models.URLField(_("Signature Photo"), blank=True, null=True)

    signature_photo_url = models.URLField(
        _("Signature Photo URL"), blank=True, null=True
    )

    def clean(self):
        super().clean()
        if self.id_issue_date and self.id_expiry_date:
            if self.id_expiry_date <= self.id_issue_date:
                raise ValidationError(_("ID expiry date must come after issue date"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def is_complete_with_next_of_kin(self):
        required_fields = [
            self.title,
            self.gender,
            self.date_of_birth,
            self.country_of_birth,
            self.place_of_birth,
            self.marital_status,
            self.means_of_identification,
            self.id_issue_date,
            self.id_expiry_date,
            self.nationality,
            self.phone_number,
            self.address,
            self.city,
            self.country,
            self.employment_status,
            self.photo,
            self.id_photo,
            self.signature_photo,
        ]
        return all(required_fields) and self.next_of_kin.exist()

    def __str__(self):
        return f"{self.title} {self.user.first_name}'s profile"


class NextOfKin(TimeStampedModel):
    class Salutation(models.TextChoices):
        MR = "mr", _("Mr")
        MRS = "mrs", _("Mrs")
        MISS = "miss", _("Miss")

    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="next_of_kin"
    )
    title = models.CharField(_("Salutation"), max_length=5, choices=Salutation.choices)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    other_name = models.CharField(_("Other Name"), max_length=50)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=10, default=Gender.choices)
    relationship = models.CharField(_("Relationship"), max_length=100)
    email_address = models.EmailField(_("Email Address"), db_index=True)
    phone_number = PhoneNumberField(_("Phone Number"))
    address = models.CharField(_("Address"), max_length=100)
    city = models.CharField(_("City"), max_length=100)
    country = CountryField(_("Country"))
    is_primary = models.BooleanField(_("Is Primary Next of Kin"), default=False)

    def clean(self):
        super().clean()
        if self.is_primary:
            primary_kin = NextOfKin.objects.filter(
                profile=self.profile, is_primary=True
            ).exclude(pk=self.pk)
            if primary_kin.exists():
                raise ValidationError(
                    _("There can be only primary next of kin per profile ")
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Next of kin for {self.profile.user.full_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "is_primary"],
                condition=models.Q(is_primary=True),
                name="Unique_primary_next_of_kin",
            )
        ]
