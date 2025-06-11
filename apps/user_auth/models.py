from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .emails import send_account_locked_email


class User(AbstractUser):
    class SecurityQuestion(models.TextChoices):
        MAIDEN_NAME = ("maiden_name", _("What is your mother's name?"))
        FAVORITE_COLR = ("favorite_colr", _("Your favorite colr?"))
        BIRT_CITY = ("birt_city", _("what is the city where you bron?"))
        CHILDHOOD_FRIEND = (
            "childhood_friend",
            _("What is the  your childhood best friends ?"),
        )

    class AccountStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        LOCKED = "locked", _("Locked")

    class RoleChoices(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        ACCOUNT_EXECUTIVE = "account_execute", _("Account Execute")
        TELLER = "teller", _("Teller")
        BRANCH_MANAGER = "branch_manager", _("Branch Manager")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_("username"), max_length=255, unique=True)
    security_question = models.CharField(
        _("Security Question"), choices=SecurityQuestion.choices, max_length=30
    )
    security_answer = models.CharField(_("security Answer"), max_length=200)
    first_name = models.CharField(
        _("First Name"), max_length=100, blank=True, null=True
    )
    email = models.EmailField(_("Email"), unique=True, db_index=True)
    middle_name = models.CharField(
        _("Middle Name"), max_length=100, blank=True, null=True
    )
    last_name = models.CharField(_("Last Name"), max_length=100)
    id_no = models.PositiveIntegerField(_("ID No"), unique=True)
    account_status = models.CharField(
        _("Account Status"),
        max_length=100,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )
    role = models.CharField(
        _("Role"),
        max_length=100,
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER,
    )
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    opt = models.CharField(_("OTP"), max_length=6, blank=True)
    opt_expiry_time = models.DateTimeField(_("OTP Expiry Time."), null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "id_no",
        "security_question",
        "security_answer",
    ]

    def send_opt(self, opt: str) -> None:
        self.opt = opt
        self.opt_expiry_time = timezone.now() + settings.OPT_EXPIRATION
        self.save()

    def verify_opt(self, opt: str) -> bool:
        if self.opt == opt and self.opt_expiry_time > timezone.now():
            self.opt = ""
            self.opt_expiry_time = None
            self.save()
            return True
        return False
